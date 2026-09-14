# JupyterLite WorldView

A browser-only teaching and demonstration environment inspired by **WorldView**, combining JupyterLite notebooks, a Jupyter Book, and a live tactical-style map dashboard.

> **Educational adaptation, not an official WorldView distribution.** This repository is designed to demonstrate geospatial dashboard patterns in a static GitHub Pages environment. It does not reproduce the original React/Express application or its credentialed data services.

## Live sites

| Experience | Live link |
|---|---|
| Landing page | https://jltobias.github.io/JupyterLite-WorldView/ |
| Live action map dashboard | https://jltobias.github.io/JupyterLite-WorldView/dashboard/ |
| JupyterLite Lab | https://jltobias.github.io/JupyterLite-WorldView/lab/index.html |
| Jupyter Book | https://jltobias.github.io/JupyterLite-WorldView/book/ |

### Launch notebooks directly

- [00 — Start here](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=00_start_here.ipynb)
- [01 — Live seismic layer](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=01_live_seismic.ipynb)
- [02 — WorldView-style dashboard](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=02_worldview_dashboard.ipynb)
- [03 — Build your own tactical layer](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=03_build_your_own_layer.ipynb)

## What this repo demonstrates

The project adapts several ideas from the original WorldView experience for a static, browser-only environment:

- dark, high-density situational-awareness styling;
- a left operations panel for layer controls and optics modes;
- a right intel feed for current events;
- a bottom status strip for coordinates, UTC time, and entity counts;
- a center targeting reticle;
- live USGS earthquake data refreshed in the browser;
- live ISS position when the public endpoint is available;
- animated **simulated** aircraft tracks for motion and interaction without requiring private APIs;
- notebook examples that explain how to build and extend these layers.

The standalone dashboard intentionally distinguishes **live** public data from **simulated** demonstration data in the UI.

## Source and attribution

This repository was created as an educational companion to the original **WorldView** project by **Kevin (Khoa) To**:

- Source repository: https://github.com/kevtoe/worldview
- Original live application: https://worldview.khoa.to
- Original license: MIT — https://github.com/kevtoe/worldview/blob/main/LICENSE
- Original README / project description: https://github.com/kevtoe/worldview/blob/main/README.md

The original project describes WorldView as a full-stack situational-awareness dashboard that brings flights, satellites, earthquakes, traffic, AIS vessels, and public CCTV feeds together on an interactive globe, with a tactical operations panel, intel feed, status bar, tracked-entity display, and visual shader modes. This repository cites that work as the design and instructional inspiration, while implementing a separate static-browser demonstration suitable for JupyterLite and GitHub Pages.

Copyright for the original WorldView project remains with **Kevin (Khoa) To (2026)** under the MIT License. See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Repository layout

```text
.
├── content/                    # JupyterLite notebooks
├── book/                       # Jupyter Book 2 / MyST source
├── dashboard/                  # standalone live tactical map
├── .github/workflows/pages.yml # builds and deploys everything to Pages
├── index.html                  # Pages landing page
├── jupyter_lite_config.json
└── requirements.txt
```

## Data notes

The dashboard uses public browser-accessible services for demonstration. USGS earthquake GeoJSON is requested live. ISS position is requested from `wheretheiss.at` and gracefully degrades when that service or browser CORS policy is unavailable. Aircraft are synthetic tracks generated in the browser and are always labeled **SIMULATED**.

No API keys are committed to this repository.

## Build locally

```bash
python -m pip install -r requirements.txt
rm -rf dist
mkdir -p dist/lab dist/book dist/dashboard
jupyter lite build --contents content --output-dir dist/lab
(cd book && jupyter book build --html)
cp -R book/_build/html/. dist/book/
cp -R dashboard/. dist/dashboard/
cp index.html dist/index.html
touch dist/.nojekyll
python -m http.server --directory dist 8000
```

Then open http://localhost:8000.

## Deployment

Pushes to `main` trigger the Pages workflow. GitHub Pages should be configured with **Source: GitHub Actions** in repository settings. The workflow builds JupyterLite and Jupyter Book, then publishes the combined `dist/` tree as one Pages site.

## License and reuse

The code written specifically for this educational demo may be reused subject to any repository-level licensing you choose to add. Third-party projects, libraries, basemap tiles, and live data services retain their own terms and attribution requirements. The original WorldView source is MIT-licensed; see the notice above and `THIRD_PARTY_NOTICES.md`.
