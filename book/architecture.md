# Architecture

The original WorldView uses a React/TypeScript/Cesium frontend plus an Express proxy to aggregate multiple public and credentialed sources. Its interface combines layer controls, an intel feed, status information, tracked entities, and display modes.

This repository deliberately chooses a smaller static architecture:

1. **GitHub Pages** serves all files.
2. **JupyterLite + Pyodide** executes Python notebooks in the browser.
3. **Leaflet** renders the standalone map.
4. **Browser fetch** retrieves public endpoints that permit cross-origin access.
5. **Synthetic tracks** fill demonstration gaps that would otherwise require credentials or a backend.

This makes the tradeoffs visible: browser CORS rules matter, secrets cannot be protected in a static site, and every layer should degrade gracefully when its upstream service is unavailable.

## Interface composition

The demo borrows the *conceptual* layout described by WorldView: operations at left, intel at right, status at bottom, central reticle, optics controls, and high-contrast tactical styling. The implementation is original to this educational repository rather than a copy of the React components.
