# Notebook curriculum

The eleven notebooks below are the full labs, including code and checked outputs. Each runs independently with the Python (Pyodide) kernel. Plan roughly 15–45 minutes per lab and 60 minutes for the capstone.

| Read the rendered lab | Execute in JupyterLite |
|---|---|
| [00 · See, calculate, explain](labs/00_start_here.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=00_start_here.ipynb) |
| [01 · Live seismic data, honest freshness](labs/01_live_seismic.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=01_live_seismic.ipynb) |
| [02 · Read the common operating picture](labs/02_worldview_dashboard.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=02_worldview_dashboard.ipynb) |
| [03 · Build a portable geospatial layer](labs/03_build_your_own_layer.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=03_build_your_own_layer.ipynb) |
| [04 · EOC: proximity, capacity, and a briefing](labs/04_eoc_response.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=04_eoc_response.ipynb) |
| [05 · Outbreak investigation: counts, rates, uncertainty](labs/05_spatial_epidemiology.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=05_spatial_epidemiology.ipynb) |
| [06 · Global health: access when roads close](labs/06_health_access.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=06_health_access.ipynb) |
| [07 · 3D scenes, extrusion, and time](labs/07_3d_scenes.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=07_3d_scenes.ipynb) |
| [08 · Astra: evidence in, reviewable briefing out](labs/08_astra_geospatial_copilot.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=08_astra_geospatial_copilot.ipynb) |
| [09 · Raster change and multimodal interpretation](labs/09_raster_change.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=09_raster_change.ipynb) |
| [10 · Capstone: an evidence-based shift handoff](labs/10_capstone.ipynb) | [Run](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=10_capstone.ipynb) |

For an introductory workshop, run 00–03. For an EOC or public-health workshop, continue with 04–06. For a visualization and AI workshop, complete 07–09. Lab 10 combines the tracks with a scored review rubric.

Use **Run → Run All Cells** in a fresh kernel. The first plotting import may download Matplotlib. Notebook HTML maps use separate iframe documents so rerunning a cell does not collide with a previous map. Full-screen dashboard links are available when a viewer restricts iframes.

The **OpenStreetMap background** checkbox turns street tiles on or off. If the tile service rejects a request or is unavailable, your data and popups remain usable against a plain background. Select the checkbox to retry, or pass `basemap=False` to `map_layer` to start without tiles. If an older notebook shows “Access blocked” images, open JupyterLite in a private window to load the corrected helper and notebooks without deleting saved work. Refreshing an existing tab may retain old browser files; replacing `worldview_lab.py` also requires restarting the kernel. See [Lab 03](labs/03_build_your_own_layer.ipynb) for details.

Output downloads appear beneath export cells. PNG files such as the raster figure can be downloaded from the file browser's `exports/` directory. A printed path alone does not copy a file to your computer.
