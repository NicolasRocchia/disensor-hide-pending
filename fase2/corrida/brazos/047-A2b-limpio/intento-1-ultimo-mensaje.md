Yes. On the primary production lines, **weld-cell-P3 accounted for 318 of 392 minutes (81%)** of servo-motor-stockout downtime. The remainder was split between assembly-cell-P1 (49 minutes) and paint-cell-P2 (25 minutes).

Even including maintenance-only equipment, weld-cell-P3 still represented 74% of the 430-minute total.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Servo-motor stockouts concentrated at weld-cell-P3",
      "description": "Weld-cell-P3 incurred 318 of 392 minutes of servo-motor-stockout downtime on primary production lines, representing approximately 81% of the total.",
      "location": "weld-cell-P3"
    }
  ]
}
```