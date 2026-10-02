# Architecture and build

![Evidence workflow](_static/generated/evidence-workflow.svg)

The upstream World View combines React/TypeScript, Cesium/Resium, and server-side services. This companion uses static hosting for JupyterLite, Leaflet, Cesium, and Jupyter Book. Public endpoints and CDN assets remain external dependencies.

| Component | Source | Responsibility |
|---|---|---|
| Canonical labs | `content/*.ipynb` | Worked analysis and visible outputs |
| Python helpers | `content/worldview_lab.py` | Distance, graph, validation, export, AI request contract |
| Scenario fixtures | `content/data/` | One consistent synthetic dataset for all experiences |
| 2D EOC | `dashboard/operations.html` | Filtering, onset window, table, GeoJSON handoff |
| 3D scene | `scenes/` | Cesium perspective, extrusion, CZML time |
| Browser helpers | `assets/lab-core.js` | Shared metrics, legends, import validation |
| Optional Astra runner | `tools/astra_brief.py` | A separate server-side API request and response validation |
| Upstream adapter | `integrations/worldview/` | Mount exports inside upstream Resium |
| Build | `scripts/build_site.py` | Assemble only public artifacts into `dist/` |

The build copies notebooks into `book/labs/` and figures into `book/_static/generated/`; these generated copies are ignored in Git. The canonical notebook outputs are refreshed through `scripts/execute_notebooks.py --write`, which runs every lab in a fresh temporary working directory. The book displays those checked outputs with execution disabled, so publishing never calls a live feed or model.

## Filesystems and browser boundaries

JupyterLite synchronizes its content into the browser kernel's filesystem. A file written to `exports/` stays in that browser environment until downloaded. The dashboards use a normal local file picker for GeoJSON. Importing a layer does not publish it, synchronize it to other operators, or save it back to GitHub.

Static pages cannot protect API secrets. The optional Astra runner is not copied to `dist/`, and no API key is required by CI. It accepts a reviewed synthetic evidence file, optionally an image, and uses credentials from a local/server process environment. It is not a public proxy.

## Verification and maintenance

Run the commands in the repository README. Unit tests cover numerical edge cases and the AI response contract. Notebook execution checks reproducibility. Browser checks serve under a repository subpath, exercise imports and controls, and capture desktop/mobile screenshots. Jupyter Book warnings fail the build. Live sources can fail independently of these checks; their status must stay explicit.
