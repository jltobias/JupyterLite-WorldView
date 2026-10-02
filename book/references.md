# References and source register

Primary references below support the methods and software interfaces. Links were reviewed on 2026-10-02. Data fixtures and figures are original synthetic exercises; citing a method does not mean the institution supplied or endorsed the scenario.

## Project and technical references

1. **To, Kevin (Khoa). WorldView (2026).** [Source](https://github.com/kevtoe/worldview), [MIT license](https://github.com/kevtoe/worldview/blob/main/LICENSE). Upstream revision inspected: `db607a44f15c037fefc4969a7fd607d7f625c171`. Design inspiration and Resium integration reference.
2. **JupyterLite documentation.** [Browser files and kernels](https://jupyterlite.readthedocs.io/en/stable/howto/content/python.html). Browser runtime and filesystem behavior.
3. **Butler et al. (2016). RFC 7946: The GeoJSON Format.** [Specification](https://www.rfc-editor.org/rfc/rfc7946). Coordinate order, geometry, and feature collections.
4. **CesiumGS. CesiumJS.** [Viewer](https://cesium.com/learn/cesiumjs/ref-doc/Viewer.html), [GeoJsonDataSource](https://cesium.com/learn/cesiumjs/ref-doc/GeoJsonDataSource.html), [CzmlDataSource](https://cesium.com/learn/cesiumjs/ref-doc/CzmlDataSource.html). Companion pins release 1.138; online documentation can describe newer releases.
5. **Leaflet.** [API reference](https://leafletjs.com/reference.html). Companion uses 1.9.4.
6. **USGS. Earthquake GeoJSON summary format.** [Documentation](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php). Event units and timestamps for the optional live feed.

## Epidemiology, EOC, and remote sensing

7. **WHO (2015). Framework for a Public Health Emergency Operations Centre.** [Publication](https://www.who.int/publications/i/item/framework-for-a-public-health-emergency-operations-centre). Institutional context; no reproduction of WHO artwork or framework text.
8. **CDC. Describing Epidemiologic Data.** [Field Epidemiology Manual chapter](https://www.cdc.gov/field-epi-manual/php/chapters/describing-epi-data.html). Descriptive analysis and interpretation by time and place.
9. **NIST/SEMATECH. e-Handbook of Statistical Methods, §7.2.4.1.** [Confidence intervals for a proportion](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm). Wilson interval formula and assumptions.
10. **WHO. AccessMod: geographic access to health care.** [Overview](https://www.who.int/tools/accessmod-geographic-access-to-health-care). Accessibility context; this repository does not use AccessMod software or results.
11. **McFeeters, S. K. (1996).** The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. *International Journal of Remote Sensing*, 17(7), 1425–1432. [doi:10.1080/01431169608948714](https://doi.org/10.1080/01431169608948714). Green/NIR index definition; bibliographic reference, no copied figures.
12. **USGS (2024).** Investigation of land cover within wetland complexes at Dixie Meadows, Churchill County, Nevada, from October 2015 to January 2022. [Report](https://pubs.usgs.gov/publication/ofr20241029/full). Additional primary context for green/NIR indices and interpretive limitations.

## OpenAI references

13. **OpenAI. GPT-6 Astra model.** [Model page](https://developers.openai.com/api/docs/models/gpt-6-astra). Supported general model capabilities and model identifier.
14. **OpenAI. Structured Outputs.** [Guide](https://developers.openai.com/api/docs/guides/structured-outputs). JSON-schema response contract.
15. **OpenAI. Images and vision.** [Guide](https://developers.openai.com/api/docs/guides/images-vision). Image input and spatial interpretation limits.
16. **OpenAI. Function calling.** [Guide](https://developers.openai.com/api/docs/guides/function-calling). Extending an application with validated tools.

Software licenses, tile terms, and data-service attribution are separately recorded in [Attribution](attribution.md) and the repository's [third-party notices](https://github.com/jltobias/JupyterLite-WorldView/blob/main/THIRD_PARTY_NOTICES.md). To cite this companion, use its [CITATION.cff](https://github.com/jltobias/JupyterLite-WorldView/blob/main/CITATION.cff).
