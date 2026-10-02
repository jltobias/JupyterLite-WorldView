# Data provenance and clocks

| Layer | Origin | Clock | Default behavior |
|---|---|---|---|
| Earthquakes in public-feed dashboard | USGS GeoJSON | Event timestamps plus retrieval | Live request, explicit failure status |
| ISS in public-feed dashboard | Where the ISS At API | Provider timestamp | Live when available; may fail under CORS/network limits |
| Aircraft in public-feed dashboard | Browser-generated routes | Animation clock | Always simulated |
| Districts, cases, facilities, roads | This repository's synthetic generator | Fixed exercise dates | Deterministic bundled data |
| Supply flight | Synthetic CZML | Sep 14, 2026, 12:00–13:00 UTC | Timeline playback |
| Raster reflectance | Seeded NumPy generator | Illustrative before/after | No real sensor or geographic claim |
| AI validation fixture | Authored notebook example | None | Not a generated model response |

The fixture manifest records definitions, CRS, dates, and limitations. Its twelve rectangular areas sit near Washington, DC solely for recognizable geographic context. They are not administrative boundaries; facility names, populations, cases, capacities, roads, and travel times are invented.

Lab 01 starts with a synthetic earthquake fallback so all labs execute reproducibly in CI. Set `USE_LIVE = True` to request USGS. Missing magnitudes remain missing, zero is preserved, and a failed request displays its fallback classification. The bundled sample is not a historical USGS snapshot.

## Reproduce or replace data

`python scripts/generate_data.py` recreates the deterministic fixtures. Daily onset counts sum exactly to district totals. Population denominators stay fixed across days. `scripts/make_assets.py` rebuilds the figures from those fixtures.

Before replacing a fixture, record the source URL, license, retrieval and observation times, geographic coverage, unit definitions, aggregation level, missingness, and transformation history. Check schema and coordinate order. A successful HTTP response is not proof of recent observation or source completeness.

Live endpoint references: [USGS format](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php), [Where the ISS At API](https://wheretheiss.at/w/developer). Provider availability, rate limits, and usage terms remain external to this project.
