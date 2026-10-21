Yes. gpu-cluster-a accounted for 947 of 1,126 NodeUnavailable failures—about 84.1%, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate",
      "severity": "major",
      "title": "NodeUnavailable concentrated on gpu-cluster-a",
      "description": "gpu-cluster-a recorded 947 of 1,126 NodeUnavailable events, approximately 84.1%.",
      "location": "customer-facing systems, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory-events aggregation."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved residue remains from this quantitative comparison."
  }
}
```