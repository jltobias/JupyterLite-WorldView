# Spatial epidemiology and global health

Mapping cases is the beginning of an investigation. Define the case, time interval, population, and geographic unit before interpreting a pattern. The [CDC descriptive epidemiology chapter](https://www.cdc.gov/field-epi-manual/php/chapters/describing-epi-data.html) provides methodological background for organizing observations by time, place, and person. All health data in these labs are invented aggregates.

![Synthetic district map, epidemic curve, and Wilson intervals with labeled axes](_static/generated/outbreak-atlas.png)

## Counts, proportions, and rates

Lab 05's numerator is new cases over 14 days. Its denominator is a fixed resident population, with at most one case per person. Dividing gives a cumulative incidence **proportion**, which we scale per 100,000. The map property `rate_per_100k` is a convenient short field name, not a claim that person-time was measured. A person-time incidence rate would require time at risk in the denominator.

Counts help describe service burden. Population-normalized quantities compare populations of different sizes. Neither establishes a cause or an individual's risk. Lab 05 includes Wilson intervals under a simple independent binomial model; they omit clustering, surveillance errors, and changing ascertainment. See the [NIST interval reference](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).

## Biases to make visible

| Issue | How it can mislead | Exercise |
|---|---|---|
| Reporting completeness | A well-observed district can look worse | Change the assumed reporting fraction |
| Denominator mismatch | Cases and population may cover different periods or boundaries | Change one denominator by ±20% |
| Reporting delay | Recent onset dates can appear artificially low | Compare onset versus report date |
| Ecological fallacy | Group patterns get attributed to individuals | Rewrite a district claim without individual inference |
| Modifiable areal unit problem | Aggregation choices change apparent patterns | Merge neighboring exercise districts |
| Small numbers | Unstable estimates look precise on a map | Inspect interval widths |

Lab 06 models access using an explicitly fictional network. The [WHO AccessMod overview](https://www.who.int/tools/accessmod-geographic-access-to-health-care) explains the broader problem of geographic access to care. Our exercise assumes undirected travel, district centroids, and fixed edge times. It does not allocate facility capacity or replace a calibrated regional accessibility model.

## Moving toward a real global-health application

Use a data dictionary and document the case definition, reporting unit, observation window, population reference year, boundary vintage, CRS, license, and missingness. Choose a locally reviewed aggregation and disclosure policy before publication. Do not put patient locations, identifiers, or sensitive small-cell tables in a public GitHub Pages site or an AI prompt. A single suppression threshold is not a complete disclosure-control method.

For possible extensions, explore [WHO's Global Health Observatory](https://www.who.int/data/gho) and [WorldPop](https://www.worldpop.org/). These datasets are not bundled or automatically ingested here; check each product's license, coverage, denominators, and update date. The capstone asks learners to justify that substitution before making a real-world claim.
