Yes. Including automated warehouse inventory, **vision-inspection-api accounted for 2,259 of 2,628 TimeoutErrors (86.0%)**. The next-largest source, `qc-label-worker`, contributed only 228 (8.7%), so the problem was strongly concentrated in one service.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in vision-inspection-api",
      "description": "vision-inspection-api generated 2,259 of 2,628 TimeoutErrors (86.0%) across non-reserved and automated warehouse inventory on 2026-10-12.",
      "location": "vision-inspection-api"
    }
  ]
}
```