Yes. FAB-3 accounted for 1,307 minutes—49.3% of all wafer-fabrication downtime, the largest share but not an outright majority. It dominated the top issue, wafer-stage vacuum instability, with 1,196 of 1,486 minutes (80.5%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "manufacturing_delays",
      "severity": "info",
      "title": "FAB-3 led wafer-fabrication downtime",
      "description": "FAB-3 recorded 1,307 of 2,651 downtime minutes. This was the largest line-level share, but slightly below a majority.",
      "location": "Wafer-fabrication delay records for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the supplied aggregate results: 1,196 vacuum-instability minutes plus 111 metrology-drift minutes."
      },
      "evidence": {
        "text": "FAB-3 contributed 1,196 minutes of vacuum-instability downtime and 111 minutes of metrology-drift downtime."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified execution gaps remain for this calculation."
  }
}
```