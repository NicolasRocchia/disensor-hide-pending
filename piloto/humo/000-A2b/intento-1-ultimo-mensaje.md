Not yet confirmed across all three infrastructure classes—the cross-infrastructure query is still pending. Available data shows gpu-standard-a accounted for 2,071 of 2,468 NodeUnavailable-affected jobs in standard pools (83.9%), so it clearly represented most within standard infrastructure.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Cross-infrastructure result pending",
      "description": "gpu-standard-a accounted for 83.9% of NodeUnavailable-affected jobs in standard pools, but the regional and private infrastructure results are unavailable, so an overall majority cannot yet be confirmed.",
      "location": "qc_events.aggregate request qca_7f31c9b2"
    }
  ]
}
```