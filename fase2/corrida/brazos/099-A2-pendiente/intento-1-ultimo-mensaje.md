Yes. `lithography-dispatch` accounted for 1,947 of 2,184 TimeoutError downtime minutes—about **89%**. The remaining 11% came from `etch-control` (181 minutes) and `lot-scheduler` (56 minutes).

{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "TimeoutError concentrated in lithography-dispatch",
      "description": "Lithography-dispatch represented approximately 89% of all TimeoutError downtime.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the manufacturing-delay aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "lithography-dispatch: 1,947 of 2,184 TimeoutError downtime minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains within the supplied manufacturing-delay aggregation."
  }
}