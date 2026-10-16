Yes. Including reserved capacity, gpu-cluster-a accounted for 2,383 of 2,883 NodeUnavailable failures—about **82.7%**, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "job_failures.aggregate_async",
      "severity": "info",
      "title": "Most NodeUnavailable failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 2,383 of 2,883 affected jobs, approximately 82.7%.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the production primary-line failure aggregation for 2026-10-12, including on-demand and reserved capacity."
      },
      "evidence": {
        "text": "NodeUnavailable: 2,883 affected jobs; gpu-cluster-a: 2,383."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions, execution gaps, or findings requiring human attention remained."
  }
}
```