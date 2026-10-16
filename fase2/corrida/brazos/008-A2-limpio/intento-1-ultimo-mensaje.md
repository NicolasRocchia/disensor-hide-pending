Yes. `gpu-cluster-a` accounted for 873 of 1,284 NodeUnavailable-affected jobs in standard pools—about **68%**, clearly a majority. Even including maintenance-only pools, it was 873 of 1,454—about **60%**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events",
      "severity": "info",
      "title": "Most NodeUnavailable impact occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 873 of 1,284 affected jobs in standard pools, or approximately 68%.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the production quality-control aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "NodeUnavailable: 1,284 affected jobs; gpu-cluster-a: 873."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified execution gaps remain for this calculation."
  }
}
```