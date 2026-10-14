Yes. Across all infrastructure, motion-control-east accounted for 401 of 512 ServoDrive-X9 stockouts—78.3%. In standard compute pools alone, it accounted for 349 of 418—83.5%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "ServoDrive-X9 stockouts concentrated in motion-control-east",
      "description": "Motion-control-east generated 401 of 512 ServoDrive-X9 stockout events across all infrastructure (78.3%), including 349 of 418 events within standard compute pools (83.5%).",
      "location": "motion-control-east"
    }
  ]
}
```