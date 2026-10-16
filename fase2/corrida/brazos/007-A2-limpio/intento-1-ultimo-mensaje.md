Yes. Rosario Final Assembly accounted for **612 of 824 minutes**, about **74.3%**, so nearly three-quarters of VacuumInterlock downtime occurred there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "production_logs",
      "severity": "info",
      "title": "Rosario had most VacuumInterlock downtime",
      "description": "Rosario Final Assembly recorded 612 of 824 total VacuumInterlock downtime minutes, approximately 74.3%.",
      "location": "Production logs for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the expanded production-footprint aggregation supplied in the conversation."
      },
      "evidence": {
        "text": "Rosario Final Assembly: 17 incidents, 612 downtime minutes; total: 824 downtime minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions, execution gaps, or interpretive judgments remain for this calculation."
  }
}
```