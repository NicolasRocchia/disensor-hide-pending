Yes. gpu-cluster-a accounted for 61 of 76 NodeUnavailable events (80.3%), affecting 366 of 438 delayed jobs (83.6%).

{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_delays.aggregate",
      "severity": "major",
      "title": "NodeUnavailable concentrated on gpu-cluster-a",
      "description": "Most NodeUnavailable failures and associated delayed jobs occurred on gpu-cluster-a.",
      "location": "Non-reserved inventory, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the inventory-delay aggregation results."
      },
      "evidence": {
        "text": "gpu-cluster-a recorded 61 of 76 events and 366 of 438 delayed jobs."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains for this conclusion within the reported non-reserved inventory data."
  }
}