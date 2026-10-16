Yes. Ashburn Assembly accounted for 2,311 of 3,000 ComponentQualificationFailure defects—about **77.0%**, so it represented a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "manufacturing_delays.aggregate_async",
      "severity": "info",
      "title": "Ashburn accounted for most defects",
      "description": "Ashburn Assembly represented 2311 of 3000 ComponentQualificationFailure defects, approximately 77.0%.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied manufacturing-delay aggregation for 2026-10-12, including internal services."
      },
      "evidence": {
        "text": "ComponentQualificationFailure: 3000 total; Ashburn Assembly: 2311."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty or execution gap remains for this calculation."
  }
}
```