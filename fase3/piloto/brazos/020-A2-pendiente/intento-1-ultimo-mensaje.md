Yes. Córdoba Assembly accounted for 1,630 of 2,846 downtime minutes—57.3% of the primary-line total. Rosario contributed 710 minutes (24.9%) and Pilar 506 minutes (17.8%). Córdoba’s result was driven mainly by vision alignment drift (1,238 minutes).

The complete-fleet query was still pending, so this conclusion applies only to the reported primary production lines.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "telemetry-review",
      "severity": "info",
      "title": "Córdoba contributed most downtime",
      "description": "Córdoba Assembly accounted for 1630 of 2846 downtime minutes, or 57.3 percent, across the primary production lines.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Calculated by summing the facility-level downtime returned by the completed telemetry aggregation."
      }
    },
    {
      "id": "h2",
      "origin": "telemetry-review",
      "severity": "minor",
      "title": "Complete-fleet result remains pending",
      "description": "The all-production-assets aggregation was accepted asynchronously but no completed result was provided.",
      "final_state": "escalated_open",
      "verification": {
        "against": "none",
        "detail": "Only an accepted request identifier was returned."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "finding_ref": "h2",
        "requires_human_attention": true,
        "description": "Confirm whether Córdoba still represents a majority after the complete-fleet telemetry request finishes.",
        "gap_reason": "other"
      }
    ]
  }
}
```