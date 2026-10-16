Yes. The TimeoutError problem was heavily concentrated in **metrology-dispatch**, which affected **1,947 of 2,297 jobs (84.8%)**. The remaining jobs were spread across lot-tracker (181), inventory-sync (113), and recipe-scheduler (56).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in metrology-dispatch",
      "description": "Metrology-dispatch accounted for 1,947 of 2,297 affected jobs, or 84.8% of the expanded quality-control scope.",
      "location": "Fab-Aurora, Fab-Cascade, and Fab-Mesa"
    }
  ]
}
```