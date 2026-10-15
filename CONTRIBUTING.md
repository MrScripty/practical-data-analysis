# Building and contributing

## Build the reading site

Use Python 3, Pandoc and Node.js. From the repository root:

```sh
python build.py
node --test tests/math.test.js
python tests/check_site.py
python -m http.server 8000 --directory docs
```

Open http://localhost:8000/. Edit manuscript chapters in `source/chapters/` and references in `source/references.md`. The builder generates the HTML site, labs, metadata and offline ZIP under `docs/`. It does not rebuild the existing downloadable PDF or analysis companion; those are separate supplied artifacts.

The browser labs use plain JavaScript and SVG. Readers need no build tools. Inputs are neither transmitted nor persisted. External references and GitHub links navigate off-site normally.

## Evidence

The scheduler examples use measured Python-simulator reports and event traces. They are not real-device or production-service benchmarks. The cohort and judge examples are explicitly synthetic. Each lab displays its data status and limitations. The downloadable companion contains the data and executable Python analysis.

## GitHub Pages

Publish `main` → `/docs` under **Settings → Pages → Deploy from a branch**. The included `.nojekyll` leaves the prebuilt HTML untouched. All asset links are relative, so this works as a project site. The offline ZIP contains the reading site and browser labs. PDF/companion downloads and external references still need a connection. Open the extracted site directly with `index.html` after extraction.

## Reuse and third-party material

No license grant is specified for this repository. Public availability alone is not a grant of unrestricted reuse. Linked papers and documentation retain their original authors' rights. Explanatory prose, examples, visualizations, and interface code are original to this book. The companion snapshot includes selected scheduler source needed to interpret the user-authorized simulator case; see its README and provenance manifest.

## Shared-link previews

Every HTML page includes static Open Graph and Twitter card metadata using a landscape book-cover card. Page-specific canonical URLs and titles are included; the image is JPEG, 1280 × 640 (230,773 bytes). The same card is saved in the repository’s Settings → Social preview. Chat and social apps control their own cropping and cache refresh timing.

