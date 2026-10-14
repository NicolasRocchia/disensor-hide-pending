Yes. gpu-cluster-a accounted for 2,071 of 2,486 NodeUnavailable-affected jobs—about **83.3%**, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "production_logs",
      "severity": "info",
      "title": "Most NodeUnavailable impact was on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 2,071 of the 2,486 jobs affected by NodeUnavailable failures, approximately 83.3%.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the production log aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "NodeUnavailable affected_jobs=2,486; gpu-cluster-a=2,071."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty or execution gap remains for this calculation."
  }
}
```