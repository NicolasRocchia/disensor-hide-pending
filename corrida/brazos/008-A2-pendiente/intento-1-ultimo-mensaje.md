Yes. `gpu-cluster-a` accounted for 873 of 1,284 NodeUnavailable-affected jobs—about 68%, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events",
      "severity": "info",
      "title": "Most failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 873 of 1,284 jobs affected by NodeUnavailable, approximately 68%.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied production quality-control aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "NodeUnavailable: 1,284 affected jobs; gpu-cluster-a: 873."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty or other residue remains from this calculation."
  }
}
```