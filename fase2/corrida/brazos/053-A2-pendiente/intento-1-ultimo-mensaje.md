Yes—within non-reserved inventory, gpu-cluster-a had 61 of 76 NodeUnavailable events (80.3%). It also accounted for 366 of 438 delayed jobs (83.6%) and 11,180 of 13,420 delay-minutes (83.3%). The reserved-capacity query had not yet returned, so this does not establish the full-inventory share.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_delays.aggregate",
      "severity": "major",
      "title": "Node failures concentrated on gpu-cluster-a",
      "description": "Gpu-cluster-a produced a clear majority of NodeUnavailable events, delayed jobs, and delay-minutes in non-reserved inventory.",
      "location": "2026-10-12 non-reserved inventory",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed inventory aggregation: 61 of 76 events, 366 of 438 delayed jobs, and 11,180 of 13,420 delay-minutes."
      },
      "evidence": {
        "text": "gpu-cluster-a: 61 events, 366 delayed jobs, 11,180 delay-minutes"
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous query covering reserved compute capacity had been accepted but no result was provided, so the full-inventory concentration remains unverified.",
        "gap_reason": "other"
      }
    ]
  }
}
```