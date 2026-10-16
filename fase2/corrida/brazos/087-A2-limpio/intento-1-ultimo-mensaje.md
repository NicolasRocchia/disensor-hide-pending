Yes. Including automated warehouse inventory, **941 of 1,396 NodeUnavailable failures (67.4%)** occurred on `gpu-cluster-a`. Excluding warehouse inventory, it was **903 of 1,284 (70.3%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events",
      "severity": "info",
      "title": "Most failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 941 of 1,396 NodeUnavailable events when automated warehouse inventory was included.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Calculated from the inventory aggregation results for 2026-10-12."
      },
      "evidence": {
        "text": "NodeUnavailable: 1,396 total; gpu-cluster-a: 941."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified interpretive judgments remain in this calculation."
  }
}
```