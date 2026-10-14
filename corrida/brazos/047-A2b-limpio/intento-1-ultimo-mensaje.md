Yes. On the reported date (October 12), **weld-cell-P3 accounted for 318 of 392 stockout minutes on primary production lines—81%**. The remaining downtime was split between assembly-cell-P1 (49 minutes) and paint-cell-P2 (25 minutes).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Servo-motor stockouts concentrated at weld-cell-P3",
      "description": "Weld-cell-P3 recorded 318 of 392 servo-motor stockout downtime minutes across primary production lines, representing approximately 81% of the total.",
      "location": "weld-cell-P3"
    }
  ]
}
```