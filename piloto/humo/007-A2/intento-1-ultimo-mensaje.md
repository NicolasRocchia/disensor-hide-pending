Yes. **2,071 of 2,486 NodeUnavailable failures—about 83.3%—occurred on gpu-cluster-a.**

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "job_failures.aggregate",
      "severity": "info",
      "title": "Most NodeUnavailable failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 2,071 of 2,486 affected jobs, approximately 83.3%.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the production primary-line aggregation for 2026-10-12."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or verification gaps remain for this calculation."
  }
}
```