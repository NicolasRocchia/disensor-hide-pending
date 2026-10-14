Yes. gpu-cluster-a accounted for 1,087 of 1,426 NodeUnavailable downtime minutes—about **76.2%**, so it caused most of that downtime.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_qc_analysis",
      "severity": "info",
      "title": "Most NodeUnavailable downtime occurred on gpu-cluster-a",
      "description": "gpu-cluster-a contributed 1,087 of 1,426 NodeUnavailable downtime minutes, approximately 76.2%.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied shipment_qc aggregate for 2026-10-12."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains for this calculation based on the supplied aggregate downtime records."
  }
}
```