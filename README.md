# Modern Classical Mechanics

An open collection of notes, activities, and computational resources for
learning and teaching classical mechanics.

## Acknowledgment

This project acknowledges the earlier work of Danny Caballero and other contributors. The present edition has been substantially revised and should not be interpreted as authored or endorsed by them.

The book is built with [MyST Markdown](https://mystmd.org/) from Jupyter
notebooks and Markdown pages. The notebooks remain the source of truth; MyST
provides the website, navigation, search, math rendering, and notebook-aware
presentation.

## Structure

- [`myst.yml`](myst.yml) — project metadata and table of contents
- [`content/index.md`](content/index.md) — book landing page
- [`content/notebooks/`](content/notebooks/) — weekly notes and homework
- [`content/images/`](content/images/) — figures referenced by the notebooks
- [`.github/workflows/`](.github/workflows/) — CI and GitHub Pages deployment

## Build

Use Node 22 (`nvm use` if you have nvm; see `.nvmrc`).

```bash
npm install
npm run start          # live preview
npm run build          # static site in _build/html/
npm run check          # production-equivalent validation build
```

For reproducible installs after `package-lock.json` exists, use `npm ci`.
Generated output is written to `_build/` and is not committed. Pull requests
are checked by CI, and pushes to `main` deploy `_build/html` to GitHub Pages.

## Print editions

The whole book can also be built as a PDF and a Word document, using the
LaTeX template in [`templates/book/`](templates/book/). Requires a TeX Live
install with XeLaTeX and latexmk for the PDF, and additionally
[pandoc](https://pandoc.org/) for the DOCX (the DOCX is built from the PDF's
intermediate `.tex` rather than MyST's own `--docx` writer, which drops
equations in as raw LaTeX strings rather than editable Word math — see
[`scripts/tex-to-docx.py`](scripts/tex-to-docx.py) for why).

```bash
npm run build:pdf      # exports/modern-classical-mechanics.pdf
npm run build:docx     # + exports/modern-classical-mechanics.docx
npm run build:exports  # both
```

`exports/` is a build artifact and is not committed; the `Exports` GitHub
Actions workflow builds it monthly, on `v*` tags, and on demand, and the
GitHub Pages deploy downloads its latest output so the site's download menu
stays populated without every push paying for a TeX Live install.

## Editing

Edit the Markdown cells in the source notebooks directly. Images referenced
from a notebook in `content/notebooks/` use paths such as
`../images/notes/week1/figure.png`. Update the `project.toc` in `myst.yml` when
adding or removing pages.

See the [MyST guide](https://mystmd.org/guide) for supported Markdown,
directives, math, figures, citations, and cross-references.

## License

The book is licensed under the
[Creative Commons Attribution-NonCommercial 4.0 International license](LICENSE)
(CC BY-NC 4.0).
