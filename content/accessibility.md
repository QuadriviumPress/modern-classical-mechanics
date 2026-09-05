# Accessibility statement

We want Modern Classical Mechanics to be usable by as many learners as possible. The project is built from open, editable sources and is published as a web edition with the original Jupyter notebooks available in the repository. Accessibility improvements are ongoing; this page describes what we support today and where work remains.

## Current support

- The site uses the semantic headings and navigation provided by the MyST book theme.
- Images in the authored Markdown and notebook text have descriptive alternative text. Decorative images should use empty alternative text; meaningful diagrams should also be explained in nearby text.
- Links use their destination or purpose as link text where possible. Video resources include a direct-link alternative.
- The source files are open so that readers can use the HTML edition, download notebooks, or adapt the content to another format.
- We preserve the underlying equations, prose, and source code so that content is not available only through a visual interaction.

## Known limitations

Some notebook-generated plots and interactive outputs still need individual text descriptions. Embedded third-party videos may have captions supplied by their publisher, but the project does not control their availability or accuracy. The theme and generated site also need testing with multiple screen readers, keyboard-only navigation, zoom, reduced motion, and high-contrast settings.

These limitations are tracked as accessibility work rather than treated as evidence that the site is fully conformant with WCAG. Please use the direct video links and the notebook source as alternatives when an embedded output is not usable.

## For contributors

When adding content:

1. Use headings in order and prefer Markdown semantics over raw HTML.
2. Give every meaningful image concise alt text that communicates its purpose. If a diagram carries information not stated in the surrounding prose, add a text explanation too.
3. Use descriptive link text such as “Euler method video” instead of “click here” or a bare URL.
4. Do not communicate information by color alone. Check contrast, focus visibility, and usability at 200% zoom.
5. Make controls usable with a keyboard and give embedded media a visible, descriptive alternative.
6. For audio or video, provide captions where possible and a transcript or detailed text summary in the source.

Before opening a pull request, run `npm run check`, inspect the rendered page with keyboard navigation, and report any remaining accessibility concern in the pull request description.

## Reporting a barrier

Please [open an accessibility issue](https://github.com/QuadriviumPress/modern-classical-mechanics/issues/new) with the page or notebook, what you expected to happen, what happened instead, and—if relevant—the browser, assistive technology, and keyboard steps involved. You can also propose a fix through a [pull request](https://github.com/QuadriviumPress/modern-classical-mechanics/pulls).
