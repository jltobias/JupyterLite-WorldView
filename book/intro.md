# WorldView · Geospatial Field Lab

![WorldView and JupyterLite field lab](_static/generated/worldview-splash.svg)

Explore emergency operations, spatial epidemiology, and global health through eleven browser-executable notebooks. Each lab connects a question to data, a calculation, a visual, and a reviewable interpretation. Maps, charts, graphs, a raster exercise, and a Cesium scene make the assumptions visible.

This educational companion is inspired by [World View by Kevin (Khoa) To](https://github.com/kevtoe/worldview), MIT. It is a separate static implementation with an adapter for loading notebook exports into the upstream application.

## Start here

- [Open the 2D EOC](https://jltobias.github.io/JupyterLite-WorldView/dashboard/operations.html).
- [Explore the 3D scene](https://jltobias.github.io/JupyterLite-WorldView/scenes/).
- [Run Lab 00 in JupyterLite](https://jltobias.github.io/JupyterLite-WorldView/lab/index.html?path=00_start_here.ipynb).
- Read the [curriculum](notebooks.md), then use the full notebooks in the book navigation.

All health scenarios are **synthetic** and contain no patient records. The public experiences need no API key. Optional GPT-6 Astra inference runs through a separate local/server runner. The [Astra chapter](astra.md) distinguishes documented capabilities, worked examples, and required verification.

The default notebooks are reproducible without live-data requests. The browser runtime and maps still need an initial network connection. This is a training environment, not an operational or clinical decision system.
