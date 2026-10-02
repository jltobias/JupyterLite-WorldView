# Emergency operations: a reviewable common picture

An EOC needs shared context across analysts, operations staff, and decision-makers. This teaching workflow uses the [WHO EOC framework](https://www.who.int/publications/i/item/framework-for-a-public-health-emergency-operations-centre) as background and demonstrates a small information workflow, not an operational command system.

![Four stages from observation to calculation, optional Astra explanation, and human review](_static/generated/evidence-workflow.svg)

Start with a question: **Which fictional facilities are near an incident, open, and represented by current exercise records?** Lab 04 calculates a spherical distance and sums capacity within a screening radius. Lab 06 adds graph travel times. Those two results answer different questions; neither proves a facility is safe or a route is usable.

## A 30-minute tabletop exercise

| Time | Role | Task | Reviewable output |
|---|---|---|---|
| 0–5 min | Situation analyst | Inspect source, window, and map legend | Data-quality notes |
| 5–15 min | GIS analyst | Run proximity and access labs | GeoJSON and numeric evidence |
| 15–20 min | Planning coordinator | Compare capacity and road-closure assumptions | List of unknowns |
| 20–25 min | Briefing author | Draft from evidence, optionally with Astra | Cited draft, labeled unreviewed |
| 25–30 min | Domain reviewer | Check units, sources, and implied actions | Revised shift handoff |

The public demo stores no shared incident state and has no multiuser authorization, dispatching, case management, or audited operational record. Adapting it for an actual EOC requires managed identity, governed data services, resilient hosting, accessibility testing, logging, continuity procedures, and local validation. The site is a training starting point.

## Read every visual as an argument

The district map makes patterns easy to see; the table allows exact comparisons. The epidemic curve separates daily counts from cumulative totals. The 3D view emphasizes differences but may hide small districts behind tall extrusions. A handoff should state what each visual encodes, when its evidence was collected, and which decision it can support.

[Open the exercise EOC](https://jltobias.github.io/JupyterLite-WorldView/dashboard/operations.html) and complete Labs 04, 06, and 10.
