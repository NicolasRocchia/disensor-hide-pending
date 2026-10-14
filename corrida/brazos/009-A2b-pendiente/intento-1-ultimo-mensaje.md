Yes. **vision-inspection-api** accounted for 1,947 of 2,184 TimeoutErrors—**89.1%**. The remainder came from qc-label-worker (181; 8.3%) and lot-release-scheduler (56; 2.6%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_analysis",
      "severity": "major",
      "title": "TimeoutErrors concentrated in vision-inspection-api",
      "description": "The service produced 1,947 of 2,184 TimeoutErrors (89.1%) in non-reserved inventory on 2026-10-12.",
      "location": "vision-inspection-api"
    }
  ]
}
```