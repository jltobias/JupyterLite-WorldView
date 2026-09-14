# Live data and provenance

The static demo is designed around transparent provenance.

## Seismic layer

Earthquakes come from the USGS M2.5+ past-day GeoJSON feed and are refreshed by the browser. Popups retain magnitude, place, depth, and a source label.

## ISS layer

The dashboard requests the current International Space Station position from the public `wheretheiss.at` API. If the endpoint or CORS policy prevents access, the status strip reports the layer as unavailable rather than fabricating a position.

## Aircraft layer

Aircraft motion is synthetic. The dashboard generates routes between representative airport coordinates so the interface can demonstrate moving entities without API keys, scraping, or a backend proxy. Every aircraft popup and count labels the data as simulated.

## Why this matters

A visual dashboard can make very different data sources look equally authoritative. Teaching examples should therefore expose whether a record is live, cached, simulated, stale, unavailable, or credential-dependent. Treat provenance as part of the user interface, not merely documentation.
