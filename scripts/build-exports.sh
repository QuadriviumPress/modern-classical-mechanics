#!/usr/bin/env bash
#
# Build the printable editions of *Modern Classical Mechanics* into exports/.
#
#   modern-classical-mechanics.pdf    the whole book as a PDF
#   modern-classical-mechanics.docx   the whole book as a Word document
#
# Usage:  scripts/build-exports.sh [pdf|docx|all]
#         npm run build:exports            (both)
#         npm run build:pdf                (PDF only)
#         npm run build:docx               (both -- the DOCX is built from the
#                                            PDF's .tex, so this rebuilds it too)
#
# Requires: Node 22 + npm 10, a Python environment with requirements.txt
# installed and a registered `python3` Jupyter kernel (the notebooks execute
# during the export, same as the website build), and a TeX Live with XeLaTeX
# and latexmk. The DOCX additionally needs pandoc; Inkscape and poppler-utils
# are needed only if a figure is ever added as an SVG (today the only SVGs are
# the GitHub badges on the landing page). See README.md.
set -euo pipefail

cd "$(dirname "$0")/.."

TARGET="${1:-all}"
OUT="exports"

step() { printf '\n\033[1m==> %s\033[0m\n' "$1"; }

build_pdf() {
  step "Building the PDF (and its intermediate .tex, for the DOCX step)"
  # --tex rather than --pdf: the export is `pdf+tex`, so this still produces
  # the PDF, and it leaves behind the .tex that the DOCX is built from.
  npx myst build --tex --execute
}

build_docx() {
  build_pdf
  step "Building the Word edition"
  python3 scripts/tex-to-docx.py
}

case "$TARGET" in
  pdf)  build_pdf ;;
  docx) build_docx ;;
  all)  build_docx ;;
  *)
    echo "usage: $0 [pdf|docx|all]" >&2
    exit 2
    ;;
esac

step "Done"
ls -lh "$OUT"/*.pdf "$OUT"/*.docx 2>/dev/null | awk '{printf "  %-52s %s\n", $9, $5}'
