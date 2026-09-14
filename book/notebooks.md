# Notebook curriculum

The JupyterLite Lab ships with four browser-executable notebooks.

## 00 — Start here

Introduces the project, explains which feeds are live versus simulated, and points to the dashboard and source attribution.

## 01 — Live seismic intelligence

Uses `pyodide.http.open_url` to retrieve USGS GeoJSON in the browser, normalizes the features into Python records, and renders a compact tactical-style event table.

## 02 — WorldView-style dashboard

Embeds the standalone dashboard for guided exploration and contrasts the original WorldView full-stack architecture with this static teaching implementation.

## 03 — Build your own tactical layer

Takes a small Python list of locations and turns it into an interactive Leaflet layer, emphasizing timestamps, provenance, confidence, filtering, and careful handling of public data.

[Open JupyterLite Lab](../lab/index.html)
