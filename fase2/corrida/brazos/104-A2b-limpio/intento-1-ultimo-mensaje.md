Yes. Across all infrastructure, **401 of 512 ServoDrive-X9 stockouts (78.3%)** occurred in `motion-control-east`. In the standard compute pools alone, the concentration was even higher: **349 of 418 (83.5%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Stockouts concentrated in motion-control-east",
      "description": "motion-control-east accounted for 401 of 512 ServoDrive-X9 stockout events across all infrastructure (78.3%).",
      "location": "motion-control-east"
    }
  ]
}
```