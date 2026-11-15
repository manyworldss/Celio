# Celio

Celio is an iPhone app that helps people with celiac disease explain what they need to the person cooking their food, in that person's language, and hear back. It works at a restaurant, at a dinner party, or on a delivery order. No account, and it works offline.

The app is in TestFlight and coming to the App Store soon. This repository holds its marketing site.

## The site

A single static page in [`site/`](site/): plain HTML, CSS and one small script. No framework and no build step.

- `site/index.html`: markup and all copy
- `site/styles.css`: design tokens (colors, type) at the top, then each section
- `site/main.js`: generates the ASCII textures and drives the scroll parallax; motion is off when Reduce Motion is on
- `site/fonts/`: self-hosted fonts (Instrument Serif, Inter, JetBrains Mono, Poppins, all under the SIL Open Font License), so the page makes no third-party requests

### Preview locally

```sh
cd site
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

### Deploy

Pushing to `main` publishes `site/` to GitHub Pages through [`.github/workflows/pages.yml`](.github/workflows/pages.yml). In the repository settings, Pages must have its source set to "GitHub Actions".

## History

Celio began as a Django web app for multilingual dietary e-cards. That version is preserved at the git tag `django-web-app-final`.

---

Celio is a communication aid, not medical advice. A Many Worlds Studio project.
