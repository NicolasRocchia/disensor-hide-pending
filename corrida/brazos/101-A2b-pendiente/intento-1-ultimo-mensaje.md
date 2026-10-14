Yes. **metrology-dispatch accounted for 1,947 of 2,184 affected jobs (89.1%)**, so the TimeoutError problem was heavily concentrated there. Lot-tracker had 181 jobs (8.3%), and recipe-scheduler had 56 (2.6%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in metrology-dispatch",
      "description": "Metrology-dispatch accounted for 1,947 of 2,184 jobs affected by TimeoutError (89.1%) on 2026-10-12.",
      "location": "Fab-Aurora, Fab-Cascade, and Fab-Mesa"
    }
  ]
}
```