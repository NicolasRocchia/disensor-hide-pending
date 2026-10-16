Yes. Motion-control-east accounted for 349 of 418 ServoDrive-X9 stockouts—83.5%. The remaining 69 occurred in assembly-orchestrator (47) and inspection-cell-standard (22).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory-reviewer",
      "severity": "info",
      "title": "ServoDrive-X9 stockouts concentrated in motion-control-east",
      "description": "Motion-control-east recorded 349 of 418 ServoDrive-X9 stockout events (83.5%).",
      "location": "standard_compute_pools/motion-control-east"
    }
  ]
}
```