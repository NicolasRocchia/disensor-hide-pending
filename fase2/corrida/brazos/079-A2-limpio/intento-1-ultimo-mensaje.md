Yes. **gpu-cluster-a accounted for 2,512 of 3,293 NodeUnavailable-affected jobs—about 76.3%**, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events",
      "severity": "info",
      "title": "Most NodeUnavailable failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 2,512 of the 3,293 jobs affected by NodeUnavailable, approximately 76.3%.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed QC aggregation for 2026-10-12, including automated warehouse inventory workflows."
      },
      "evidence": {
        "text": "NodeUnavailable: 3,293 affected jobs total; gpu-cluster-a: 2,512."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified execution gaps remain for this calculation."
  }
}
```