Yes. **metrology-dispatch accounted for 1,947 of 2,184 affected jobs—about 89%**. The remainder involved lot-tracker (181 jobs) and recipe-scheduler (56 jobs).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant-reviewer",
      "severity": "major",
      "title": "TimeoutError concentrated in metrology-dispatch",
      "description": "Metrology-dispatch accounted for 1,947 of 2,184 jobs affected by TimeoutError, approximately 89%.",
      "location": "Fab-Aurora, Fab-Cascade, and Fab-Mesa; quality-control events for 2026-10-12"
    }
  ]
}
```