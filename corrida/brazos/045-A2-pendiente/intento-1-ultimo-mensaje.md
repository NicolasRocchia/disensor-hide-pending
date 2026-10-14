Yes. Of 2,184 `TimeoutError` events, 1,947 occurred in `dispatch-api`—about **89.1%**. `customer-tracking` had 181 (8.3%), and `label-scheduler` had 56 (2.6%). This confirms strong concentration in `dispatch-api` within the customer-facing systems reviewed. The broader regional/private-infrastructure query had not completed.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_records.aggregate",
      "severity": "major",
      "title": "TimeoutError concentrated in dispatch-api",
      "description": "dispatch-api accounted for 1,947 of 2,184 TimeoutError events, approximately 89.1 percent.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied shipment-record aggregation for customer-facing systems."
      },
      "evidence": {
        "text": "TimeoutError: dispatch-api 1,947; customer-tracking 181; label-scheduler 56."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous query covering regional or private infrastructure was accepted, but no completed result was provided.",
        "gap_reason": "other"
      }
    ]
  }
}
```