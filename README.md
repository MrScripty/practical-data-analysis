# Practical Data Analysis for Engineering Decisions

A static, accessible reading edition with nine interactive examples embedded in the chapters. The expanded edition has 18 chapters, a mathematical reference, 16 figures, and a 100-page downloadable PDF.

- **Read:** https://mrscripty.github.io/practical-data-analysis/
- **Site:** `docs/` is the complete GitHub Pages publishing directory
- **Manuscript:** `source/chapters/` and `source/references.md`
- **Build:** Python 3 and Pandoc; run `python build.py`
- **Test:** Node.js; run `node --test tests/math.test.js`, then `python tests/check_site.py`

The browser labs use plain JavaScript and SVG. No package install, analytics, cookies, external font service, model API, server, or login is required to read or use them. User input is neither transmitted nor persisted. Links to references and GitHub navigate to external sites in the usual way.

## Evidence

The scheduler examples use measured Python-simulator reports and event traces. They are not real-device or production-service benchmarks. The cohort and judge examples are explicitly synthetic. Each lab displays its data status and limitations. The downloadable companion contains the data and executable Python analysis.

## GitHub Pages

Publish `main` → `/docs` under **Settings → Pages → Deploy from a branch**. The included `.nojekyll` leaves the prebuilt HTML untouched. All asset links are relative, so this works as a project site. The offline ZIP contains the reading site and browser labs. PDF/companion downloads and external references still need a connection. Open the extracted site directly with `index.html` after extraction.

## Reuse and third-party material

No license grant is specified for this repository. Public availability alone is not a grant of unrestricted reuse. Linked papers and documentation retain their original authors' rights. Explanatory prose, examples, visualizations, and interface code are original to this book. The companion snapshot includes selected scheduler source needed to interpret the user-authorized simulator case; see its README and provenance manifest.

## Shared-link previews

Every HTML page includes static Open Graph and Twitter card metadata using the intact public book cover. Page-specific canonical URLs and titles are included; the image is PNG, 1102 × 1427. Chat and social apps control their own cropping and cache refresh timing.
