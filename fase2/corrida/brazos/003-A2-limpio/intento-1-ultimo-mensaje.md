Yes. Across primary and secondary production lines, **cell-orion accounted for 2,341 of 2,751 `NodeUnavailable` failures—85.1%**. The remainder was split between cell-polaris (262; 9.5%) and cell-vega (148; 5.4%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "job_failures.aggregate_async",
      "severity": "major",
      "title": "NodeUnavailable concentrated in cell-orion",
      "description": "Cell-orion produced 85.1% of all NodeUnavailable failures across primary and secondary production lines.",
      "location": "production/cell-orion",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the aggregated production job-failure record for 2026-10-12."
      },
      "evidence": {
        "text": "NodeUnavailable: cell-orion 2,341; cell-polaris 262; cell-vega 148; total 2,751."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains for the production-cell concentration question."
  }
}
```