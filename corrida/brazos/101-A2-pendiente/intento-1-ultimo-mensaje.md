Yes. `metrology-dispatch` accounted for 1,947 of 2,184 affected jobs—about **89.1%**. The remainder was split between `lot-tracker` (181; 8.3%) and `recipe-scheduler` (56; 2.6%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate",
      "severity": "info",
      "title": "TimeoutError concentrated in metrology-dispatch",
      "description": "Metrology-dispatch represented 1,947 of the 2,184 jobs affected by TimeoutError, approximately 89.1 percent.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied quality-control aggregation result for 2026-10-12."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains within the supplied quality-control aggregation data."
  }
}
```