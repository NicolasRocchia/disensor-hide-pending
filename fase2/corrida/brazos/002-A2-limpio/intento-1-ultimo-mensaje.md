Yes. Including reserved compute capacity, **699 of 914 NodeUnavailable failures (76.5%)** occurred on `gpu-cluster-a`. For non-reserved inventory alone, it was **611 of 742 (82.3%)**.

{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events",
      "severity": "major",
      "title": "Most NodeUnavailable failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 699 of 914 NodeUnavailable events across the complete inventory scope.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed inventory aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "NodeUnavailable: 914 total events; gpu-cluster-a: 699 events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified execution gaps remained after reviewing the completed aggregation."
  }
}