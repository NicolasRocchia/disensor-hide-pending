Yes. The TimeoutError problem was highly concentrated in `vision-inspection-api`: **1,947 of 2,184 events (89.1%)**. The remainder came from `qc-label-worker` (181; 8.3%) and `lot-release-scheduler` (56; 2.6%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_event_reviewer",
      "severity": "major",
      "title": "TimeoutErrors concentrated in vision-inspection-api",
      "description": "vision-inspection-api generated 1,947 of 2,184 TimeoutError events (89.1%) in non-reserved inventory on 2026-10-12.",
      "location": "vision-inspection-api"
    }
  ]
}
```