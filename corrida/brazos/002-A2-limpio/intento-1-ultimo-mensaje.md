Yes. Including reserved compute capacity, **699 of 914 NodeUnavailable failures (76.5%)** occurred on `gpu-cluster-a`. For non-reserved inventory alone, it was **611 of 742 (82.3%)**.

{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate_async",
      "severity": "info",
      "title": "Most failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 699 of 914 NodeUnavailable events, or 76.5%.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed inventory aggregation for 2026-10-12."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty or execution gap remains for this calculation."
  }
}