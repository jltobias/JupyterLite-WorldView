# 3D scenes and interoperability

[Open the scene lab](https://jltobias.github.io/JupyterLite-WorldView/scenes/) to explore CesiumJS 1.138, the same rendering family used by the original World View. The companion loads an ellipsoid globe and Cesium's bundled Natural Earth imagery. No ion token, terrain stream, Google Photorealistic 3D Tiles, or private imagery service is configured.

## What the scene encodes

| Element | Meaning | Units and limits |
|---|---|---|
| District footprint | Fictional teaching geography | WGS 84 longitude/latitude |
| Extrusion height | Cumulative new cases / 100,000 × 5 | Metres used only as display units |
| District color | Same fixed bins as the 2D map | <200, 200–399, ≥400 per 100,000 |
| Onset-day slider | Cumulative cases from September 1 to selected day | 1–14 September 2026 |
| Supply flight | Synthetic CZML time samples | September 14, 12:00–13:00 UTC |
| Flight height | Illustrative ellipsoid altitude | Metres; not a navigable route |

Use 3D, 2D, and Columbus view to compare perspective and occlusion. The district buttons offer exact values without picking a polygon. The 2D EOC includes a complete table. The flight timeline and onset-day slider intentionally represent different clocks; moving one does not move the other.

## From a notebook to a scene

Lab 03 exports a Point GeoJSON layer. Lab 07 exports district polygons with `height_m` and a CZML document with timestamped positions. Download a GeoJSON export and import it with the scene's file picker. Files stay in that tab and are not uploaded to a service. Imported source claims are labeled unverified. The importer supports Point and Polygon only and caps size and geometry complexity.

To modify the route in this companion, edit `content/data/response.czml` and rebuild. The UI intentionally imports GeoJSON only; it does not claim a general CZML file importer. For upstream World View integration, follow the [adapter guide](https://github.com/jltobias/JupyterLite-WorldView/tree/main/integrations/worldview). The adapter mounts within upstream `GlobeViewer` and owns its data source without replacing existing live layers.

## Further scene experiments

Change the height scale and inspect the 2D reference before choosing an encoding. Compare linear route interpolation with denser samples. Introduce a missing day and decide whether to show no data, interpolate, or carry values forward; document the choice. Add 3D Tiles only after checking provider terms, attribution, costs, coordinate reference, and token scope.

References: [Cesium Viewer](https://cesium.com/learn/cesiumjs/ref-doc/Viewer.html), [GeoJSON data source](https://cesium.com/learn/cesiumjs/ref-doc/GeoJsonDataSource.html), [CZML data source](https://cesium.com/learn/cesiumjs/ref-doc/CzmlDataSource.html).
