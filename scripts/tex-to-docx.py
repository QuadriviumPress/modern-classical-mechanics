#!/usr/bin/env python3
"""Turn the LaTeX export of *Modern Classical Mechanics* into a Word document.

Why not ``myst build --docx``
------------------------------
MyST's own DOCX renderer writes every equation as ``Math(MathRun(latex))`` --
the raw LaTeX *string* dropped inside a Word equation field. Word shows
``\\frac{3\\lambda}{d}``, not a fraction, and the only cure is to select each
equation and hit Convert -> Professional by hand. This book runs to several
hundred display equations and thousands of inline ones, so that renderer is
not usable here.

Pandoc's LaTeX reader converts the same math to OMML, which Word renders and
edits natively. So the DOCX is built from the ``.tex`` that already produced
the PDF -- one source, one set of numbers, one set of cross-references.

Two things have to be fixed up before pandoc will take that file:

1. **The preamble.** Pandoc is asked to read a body, not typeset the book, so
   it is given a minimal preamble rather than templates/book/template.tex.
2. **``\\include``.** The book is a master file plus one file per page. They
   are concatenated here rather than left to pandoc's include handling, which
   resolves paths relative to the working directory.

A third fix-up, rasterizing PDF figures to PNG, is a no-op for this book's own
content -- every local figure is already a PNG or JPG that Word embeds
directly -- but is kept for the handful of SVGs (the GitHub badges on the
landing page) that MyST's tex export converts to PDF via Inkscape, which Word
cannot display at all.

Usage::

    python3 scripts/tex-to-docx.py [--tex-dir DIR] [--output FILE] [--dpi N]

Run it after ``myst build --tex``, or let ``scripts/build-exports.sh`` drive
it.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

PREAMBLE = "\n".join(
    [
        r"\documentclass{book}",
        r"\usepackage{amsmath}",
        r"\usepackage{amssymb}",
        r"\usepackage{graphicx}",
        r"\usepackage{hyperref}",
        # myst-to-tex renders a markdown thematic break (`---`) as
        # `\centerline{\rule{13cm}{0.4pt}}`. Both are plain-TeX/LaTeX
        # primitives pandoc's reader does not know by default; give it a
        # one-argument stub for each so it renders as a plain paragraph rule
        # rather than aborting the whole file.
        r"\newcommand{\centerline}[1]{#1}",
        r"\newcommand{\rule}[2]{\hrulefill}",
        r"\begin{document}",
        "",
    ]
)


def flatten(master: Path) -> str:
    """Return the document body of *master* with every ``\\include`` resolved."""
    source = master.read_text(encoding="utf-8")
    start = source.index(r"\begin{document}") + len(r"\begin{document}")
    body = source[start : source.rindex(r"\end{document}")]

    def substitute(match: re.Match[str]) -> str:
        included = master.parent / f"{match.group(1)}.tex"
        if not included.exists():
            print(f"  warning: \\include{{{match.group(1)}}} not found", file=sys.stderr)
            return ""
        return included.read_text(encoding="utf-8")

    body = re.sub(r"\\include\{([^}]+)\}", substitute, body)

    # The two `level: -1` part dividers ("Course Information", "Homework" in
    # myst.yml) render as `\part{...}`, which in LaTeX book class sits above
    # \chapter without disturbing its numbering. Pandoc's reader has no such
    # concept: it treats \part as the outermost heading level and nests every
    # following \chapter beneath it as a subsection, so everything from
    # "Course Information" on collapses into one heading tree instead of a
    # flat, consecutively numbered chapter list. `\chapter*` -- an unnumbered
    # chapter heading, a sibling of \chapter rather than a parent -- is what
    # pandoc needs to see instead.
    body = re.sub(r"\\part\{", r"\\chapter*{", body)

    # Every `[a linked image](url)` -- a YouTube thumbnail, a source badge --
    # renders as `\href{url}{\includegraphics{...}\n\n...}`: myst-to-tex
    # closes the image's own block *inside* the href's argument, leaving a
    # blank line right after `\includegraphics`. LaTeX does not care, but
    # pandoc's reader treats a blank line as a paragraph break, which is
    # illegal inside a macro argument, and refuses the whole file over it.
    # Anchoring on `\includegraphics` itself (rather than the closing brace,
    # which sometimes carries stray trailing punctuation from the link text)
    # catches every case regardless of what follows.
    return re.sub(r"(\\includegraphics\[[^\]]*\]\{[^}]*\})\n[ \t]*\n", r"\1\n", body)


def rasterize(body: str, tex_dir: Path, out_dir: Path, dpi: int) -> str:
    """Convert every PDF figure the body references to PNG, and repoint it.

    Word has no PDF image support: a ``\\includegraphics{...pdf}`` left alone
    lands as an empty frame. The only PDFs in this book's export are SVGs
    (the landing page's GitHub badges) that MyST converted for the print
    edition, so this is a no-op whenever none are referenced.
    """
    referenced = sorted(set(re.findall(r"\{(files/[^}]+\.pdf)\}", body)))
    if not referenced:
        return body

    # poppler's pdftoppm before ImageMagick: Ubuntu ships an ImageMagick policy
    # that refuses to read PDF at all (it delegates to Ghostscript), so the
    # ImageMagick path works on a developer's machine and silently produces a
    # figureless Word file on a CI runner. pdftoppm has no such policy, renders
    # onto white, and is faster.
    if shutil.which("pdftoppm"):
        command = lambda src, dst: [
            "pdftoppm", "-png", "-singlefile", "-r", str(dpi), str(src), str(dst.with_suffix("")),
        ]
    elif shutil.which("magick") or shutil.which("convert"):
        magick = shutil.which("magick") or shutil.which("convert")
        command = lambda src, dst: [
            magick, "-density", str(dpi), str(src),
            # PDF figures have a transparent background; Word renders that as
            # black unless it is flattened to white first.
            "-background", "white", "-alpha", "remove", "-alpha", "off", str(dst),
        ]
    else:
        print(
            "  warning: neither pdftoppm (poppler-utils) nor ImageMagick found; "
            "the DOCX will be missing figures",
            file=sys.stderr,
        )
        return body

    (out_dir / "files").mkdir(parents=True, exist_ok=True)
    print(f"  rasterizing {len(referenced)} figure(s) at {dpi} dpi")
    for relative in referenced:
        target = out_dir / relative.replace(".pdf", ".png")
        if target.exists():
            continue
        subprocess.run(command(tex_dir / relative, target), check=True, capture_output=True)
    return body.replace(".pdf}", ".png}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tex-dir",
        type=Path,
        default=Path("exports/modern-classical-mechanics_pdf_tex"),
        help="directory holding the MyST LaTeX export (default: %(default)s)",
    )
    parser.add_argument(
        "--master",
        default="modern-classical-mechanics.tex",
        help="master .tex file inside --tex-dir (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("exports/modern-classical-mechanics.docx"),
        help="Word file to write (default: %(default)s)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="resolution for rasterized figures (default: %(default)s)",
    )
    args = parser.parse_args()

    master = args.tex_dir / args.master
    if not master.exists():
        print(f"{master} not found -- run `myst build --tex` first.", file=sys.stderr)
        return 1
    if not shutil.which("pandoc"):
        print("pandoc is not installed; see README.md.", file=sys.stderr)
        return 1

    work = args.tex_dir / "_docx"
    work.mkdir(parents=True, exist_ok=True)

    print(f"Assembling {master} for pandoc")
    body = rasterize(flatten(master), args.tex_dir, work, args.dpi)
    flat = work / "flat.tex"
    flat.write_text(PREAMBLE + body + "\n\\end{document}\n", encoding="utf-8")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    print(f"Converting to {args.output}")
    result = subprocess.run(
        [
            "pandoc",
            "--from=latex",
            "--to=docx",
            "--toc",
            "--toc-depth=2",
            # Numbered headings, so the Word file's 4.1, 4.2 ... match the PDF's
            # and the website's, which the prose refers to by number.
            "--number-sections",
            # Rasterized figures live in the work directory; the PNGs and JPGs
            # already in the export, which need no conversion, are still in
            # the export directory. Pandoc silently drops an image it cannot
            # find, so it has to be told about both.
            "--resource-path", f"{work.resolve()}:{args.tex_dir.resolve()}",
            str(flat.name),
            "-o", str(args.output.resolve()),
        ],
        cwd=work,
    )
    if result.returncode:
        return result.returncode

    print(f"Wrote {args.output} ({args.output.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
