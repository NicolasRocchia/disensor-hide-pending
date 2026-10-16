Yes. On October 12, 2026, gpu-cluster-a accounted for 2,383 of 2,883 NodeUnavailable failures—about 82.7%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Most NodeUnavailable failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 2,383 of 2,883 affected jobs, or approximately 82.7%.",
      "location": "production / primary lines / on-demand and reserved capacity"
    }
  ]
}
```