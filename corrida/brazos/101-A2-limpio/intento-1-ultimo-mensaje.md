Yes. **Metrology-dispatch accounted for 1,947 of 2,297 affected jobs—84.8%**. The remainder was split among lot-tracker (181), inventory-sync (113), and recipe-scheduler (56). So the TimeoutError problem was strongly concentrated in metrology-dispatch.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in metrology-dispatch",
      "description": "Metrology-dispatch represented 84.8% of all jobs affected by TimeoutError on 2026-10-12.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed quality-control aggregation covering fabrication and automated warehouse inventory."
      },
      "evidence": {
        "text": "TimeoutError affected 2,297 jobs, including 1,947 attributed to metrology-dispatch."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remained after checking the completed aggregation results."
  }
}
```