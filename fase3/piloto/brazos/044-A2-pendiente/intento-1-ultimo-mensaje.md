Yes. In standard compute pools on October 12, `fab-shipment-router` accounted for 1,947 of 2,184 TimeoutError-affected jobs—about **89.1%**. The remaining 237 were split between `carrier-label-worker` (181) and `dock-slot-scheduler` (56).

The broader query including internal services had not returned, so this conclusion is limited to the completed dataset.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_analytics",
      "severity": "info",
      "title": "TimeoutErrors concentrated in fab-shipment-router",
      "description": "The service accounted for approximately 89.1% of TimeoutError-affected jobs in standard compute pools.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed aggregate_failures query for 2026-10-12."
      },
      "evidence": {
        "text": "fab-shipment-router affected 1,947 of the 2,184 jobs impacted by TimeoutError."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous query extending coverage to internal services had not returned, so the concentration beyond the completed standard-pool dataset remains unverified.",
        "gap_reason": "other"
      }
    ]
  }
}
```