Yes. **metrology-dispatch accounted for 1,947 of 2,297 affected jobs—84.8%**. The remainder was split among lot-tracker (181; 7.9%), inventory-sync (113; 4.9%), and recipe-scheduler (56; 2.4%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate",
      "severity": "major",
      "title": "TimeoutError concentrated in metrology-dispatch",
      "description": "Metrology-dispatch represented 84.8% of all jobs affected by TimeoutError across the expanded quality-control scope.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the reported service breakdown: 1,947 divided by 2,297 affected jobs."
      },
      "evidence": {
        "text": "TimeoutError affected 2,297 jobs, including 1,947 attributed to metrology-dispatch."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains in the reported service-level concentration calculation."
  }
}
```