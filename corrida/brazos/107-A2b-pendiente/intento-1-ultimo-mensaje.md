Yes. **fab-line-p1 accounted for 1,917 of 2,284 WaferCarrierRouteTimeout delays—about 84%** across the primary production lines. The advanced-packaging query was still pending, so this conclusion applies only to the completed primary-line results.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Fab-line-p1 dominated wafer routing delays",
      "description": "Fab-line-p1 accounted for 1,917 of 2,284 WaferCarrierRouteTimeout-affected jobs, approximately 84 percent.",
      "location": "primary_production_lines/fab-line-p1"
    }
  ]
}
```