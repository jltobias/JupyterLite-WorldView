# Load notebook exports in the original World View

This companion remains a separate static application. The adapter provides an explicit integration with [kevtoe/worldview](https://github.com/kevtoe/worldview), inspected at commit `db607a44f15c037fefc4969a7fd607d7f625c171` on 2026-10-02. Its `src/components/globe/GlobeViewer.tsx` renders `children` inside Resium's `Viewer`, which supplies the Cesium context used here.

1. In your own upstream checkout, follow its installation and environment instructions. Keep the original MIT notice.
2. Copy `NotebookLayer.tsx` into `src/components/globe/`.
3. Download Lab 07's `extruded-districts.geojson` and `supply-flight.czml`. Review them, then put them in the upstream checkout's `public/lab/` directory.
4. Import the component where you render `GlobeViewer` (normally `src/App.tsx`) and add it among that viewer's children:

```tsx
import NotebookLayer from './components/globe/NotebookLayer';

// Inside the existing <GlobeViewer ...> element:
<NotebookLayer url="/lab/extruded-districts.geojson" format="geojson" />
<NotebookLayer url="/lab/supply-flight.czml" format="czml" />
```

The adapter adds/removes only the data source it owns; it does not reset upstream live layers, camera, or clock. Add your own status display via a stable `onError` callback. For CZML playback, the upstream viewer's clock must be set to the document interval (2026-09-14 12:00–13:00 UTC) and advanced; the companion's standalone scene already includes that timeline. Otherwise the time-limited flight will be outside the current clock and invisible.

GeoJSON polygon `height_m` is an illustrative attribute, capped at 100 km for display. It is unrelated to terrain. This adapter is source-level integration, not a plugin installer or a complete fork of World View. Check it against your chosen upstream version and run its normal TypeScript/build checks. Live flights, vessels, CCTV, photorealistic tiles, and their provider accounts remain upstream responsibilities.

Adapter code: MIT, this repository. Upstream World View: MIT, Kevin (Khoa) To. CesiumJS: Apache-2.0; Resium: MIT. No upstream source files were copied into this companion.
