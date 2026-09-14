# JupyterLite WorldView

This book documents a browser-only educational adaptation of the ideas demonstrated by [WorldView](https://github.com/kevtoe/worldview), the MIT-licensed situational-awareness project by Kevin (Khoa) To.

The companion site includes a tactical-style live map, JupyterLite notebooks, and this book. The goal is to make the architecture and design patterns easy to study without requiring a backend server or private API keys.

## Open the experiences

- [Live action map dashboard](../dashboard/)
- [JupyterLite Lab](../lab/index.html)
- [Source repository](https://github.com/jltobias/JupyterLite-WorldView)

The demo separates live public data from simulated data. USGS seismic events are live; ISS position is requested live when its public endpoint is reachable; aircraft tracks are synthetic and labeled **SIMULATED**.
