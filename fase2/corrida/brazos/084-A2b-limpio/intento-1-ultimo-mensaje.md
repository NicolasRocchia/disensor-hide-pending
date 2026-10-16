Yes. Across primary and secondary lines, **pallet-vision-api accounted for 1,602 of 1,972 TimeoutError downtime minutes—81%**. The other services contributed much less:

- weigh-station-gateway: 243 minutes (12%)
- label-verification-service: 127 minutes (6%)

The concentration was even stronger on primary lines, where pallet-vision-api caused 1,218 of 1,436 minutes (85%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutError downtime concentrated in pallet-vision-api",
      "description": "Pallet-vision-api accounted for 1,602 of 1,972 TimeoutError downtime minutes across primary and secondary production lines, approximately 81%.",
      "location": "External services on primary and secondary production lines, 2026-10-12"
    }
  ]
}
```