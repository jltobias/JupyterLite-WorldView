# Third-party notices and attribution

## Original World View

[World View](https://github.com/kevtoe/worldview), copyright (c) 2026 **Kevin (Khoa) To**, MIT. Inspected revision: `db607a44f15c037fefc4969a7fd607d7f625c171` (2026-10-02). Conceptual interface and Cesium architecture inspired this independent companion. The upstream application is not redistributed here. Its complete [MIT notice](licenses/WORLDVIEW-MIT.txt) is retained; [authoritative source](https://github.com/kevtoe/worldview/blob/main/LICENSE).

## Software

| Component | Version/range used | License and source |
|---|---|---|
| CesiumJS | 1.138, CDN | [Apache-2.0 and bundled notices](licenses/CESIUM-Apache-2.0.txt); [source](https://github.com/CesiumGS/cesium/tree/1.138) |
| Leaflet | 1.9.4, CDN | [BSD-2-Clause notice](licenses/LEAFLET-BSD-2-Clause.txt); [source](https://github.com/Leaflet/Leaflet/tree/v1.9.4) |
| JupyterLite core | 0.6.x | [BSD-3-Clause notice](licenses/JUPYTERLITE-BSD-3-Clause.txt); [source](https://github.com/jupyterlite/jupyterlite) |
| JupyterLite Pyodide kernel | 0.6.x | [BSD-3-Clause](https://github.com/jupyterlite/pyodide-kernel/blob/main/LICENSE) |
| JupyterLab / Jupyter Book | Lite distribution / Book 1.x | [JupyterLab BSD-3-Clause](https://github.com/jupyterlab/jupyterlab/blob/main/LICENSE), [Jupyter Book BSD-3-Clause](https://github.com/jupyter-book/jupyter-book/blob/v1.0.4/LICENSE) |
| Pyodide | Selected by kernel distribution | [MPL-2.0 notice](licenses/PYODIDE-MPL-2.0.txt); [source](https://github.com/pyodide/pyodide) |
| Matplotlib | 3.x, runtime-dependent | [PSF-based license and bundled notices](https://matplotlib.org/stable/project/license.html) |
| NumPy | Runtime-dependent | [BSD-3-Clause](https://numpy.org/doc/stable/license.html) |
| IPython | Runtime-dependent | [BSD-3-Clause](https://github.com/ipython/ipython/blob/main/COPYING.rst) |
| Resium | Upstream adapter only | [MIT](https://github.com/reearth/resium/blob/main/LICENSE) |

Dependencies and CDN bundles retain their own copyright notices and any included third-party licenses. This inventory identifies direct teaching/rendering components, not every transitive package. Preserve the licenses in built distributions when redistributing them. No vendor code is relicensed under the companion's MIT license.

## Maps, imagery, and services

- **OpenStreetMap:** © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright). Map data under ODbL; rendered tiles have separate [tile usage requirements](https://operations.osmfoundation.org/policies/tiles/). No offline tile cache or bulk downloader is supplied.
- **CARTO:** basemap tiles in the original public-feed dashboard; attribution to [CARTO](https://carto.com/attributions) and OpenStreetMap. Check [service terms](https://carto.com/legal/) before operational or high-volume reuse.
- **Natural Earth:** [public-domain map data](https://www.naturalearthdata.com/about/terms-of-use/), bundled in Cesium's low-resolution imagery. It is a basemap, not current event evidence.
- **USGS:** [earthquake feed and format](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php); [copyrights and credits](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits). USGS source attribution is retained for live data. The bundled fallback is our synthetic fixture, not a USGS data product.
- **Where the ISS At:** [API documentation](https://wheretheiss.at/w/developer). This repository does not claim ownership of provider data or waive its service conditions.
- **OpenAI:** [GPT-6 Astra documentation](https://developers.openai.com/api/docs/models/gpt-6-astra) and [service terms](https://openai.com/policies/services-agreement/). Optional inference requires the operator's own access; no model weights, API entitlement, or usage credit is included.

WHO, CDC, NIST, IETF, and research papers are cited for background. Their text and figures are not reproduced or relicensed. See [book/references.md](book/references.md).

## Original companion material

Code, notebooks, documentation, synthetic fixtures, and original illustrations/plots: copyright (c) 2026 James Tobias and JupyterLite WorldView contributors, [MIT](LICENSE). `assets/worldview-splash.svg` and `assets/evidence-workflow.svg` are original vector illustrations. `assets/outbreak-atlas.png` and notebook plots are generated from synthetic data with Matplotlib. No original World View screenshots, institutional logos, patient data, or real case locations are included.

The MIT license does not grant rights to third-party brands, hosted services, restricted data, or provider accounts. No affiliation or endorsement is implied.
