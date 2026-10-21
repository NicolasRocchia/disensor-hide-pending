Yes. Córdoba Assembly accounted for 214 of 286 SD-48 stockout events—about **74.8%**. Rosario Components and Pilar Final Test together accounted for the remaining 72 events (25.2%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Córdoba produced most SD-48 stockouts",
      "description": "Córdoba Assembly recorded 214 of the 286 SD-48 stockout events, representing approximately 74.8% of the total.",
      "location": "Production inventory logs for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated 214 divided by 286 from the supplied production-log aggregation."
      },
      "evidence": {
        "text": "SD-48 servo drive: 286 total events; Córdoba Assembly: 214 events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified conclusions remain from this calculation."
  }
}
```