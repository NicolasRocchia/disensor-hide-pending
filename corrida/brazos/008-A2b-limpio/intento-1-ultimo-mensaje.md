Yes. gpu-cluster-a accounted for 873 of 1,454 NodeUnavailable-affected jobs—about 60%. Among standard pools alone, it was 873 of 1,284, or 68%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Most NodeUnavailable impact was on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 873 of 1,454 affected jobs across standard and maintenance-only pools.",
      "location": "production compute pools, 2026-10-12"
    }
  ]
}
```