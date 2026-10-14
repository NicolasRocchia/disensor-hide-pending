Yes. **metrology-dispatch accounted for 1,947 of 2,297 affected jobs—84.8%** of the TimeoutError impact. The remainder came from lot-tracker (181), inventory-sync (113), and recipe-scheduler (56).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutError concentrated in metrology-dispatch",
      "description": "Metrology-dispatch accounted for 1,947 of 2,297 affected jobs (84.8%), indicating that the TimeoutError problem was strongly concentrated in one service.",
      "location": "QC events for 2026-10-12 across Fab-Aurora, Fab-Cascade, and Fab-Mesa"
    }
  ]
}
```