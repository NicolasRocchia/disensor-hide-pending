Yes. For non-reserved inventory on 2026-10-12, `vision-inspection-api` produced 1,947 of 2,184 `TimeoutError` events—89.1%.

The remainder came from `qc-label-worker` (181; 8.3%) and `lot-release-scheduler` (56; 2.6%). The broader query including automated-warehouse inventory had not returned, so this conclusion is limited to non-reserved inventory.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate",
      "severity": "major",
      "title": "Timeout errors concentrated in vision inspection",
      "description": "The vision-inspection-api generated 89.1% of TimeoutError events in non-reserved inventory.",
      "location": "Quality-control telemetry for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the returned aggregate of 2,184 TimeoutError events grouped by service."
      },
      "evidence": {
        "text": "vision-inspection-api recorded 1,947 of 2,184 TimeoutError events."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous aggregate including automated-warehouse inventory had not returned, so concentration across the expanded inventory scope remains unverified.",
        "gap_reason": "other"
      }
    ]
  }
}
```