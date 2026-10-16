Yes. In customer-facing systems, **dispatch-api accounted for 1,947 of 2,184 TimeoutErrors—89.1%**. Customer-tracking had 181 (8.3%), and label-scheduler had 56 (2.6%). The problem was strongly concentrated in dispatch-api.

The broader regional/private-infrastructure query had not completed, so this conclusion is limited to customer-facing systems.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_records.aggregate",
      "severity": "info",
      "title": "TimeoutErrors concentrated in dispatch-api",
      "description": "Dispatch-api produced 1,947 of 2,184 TimeoutError events (89.1%) in customer-facing systems on 2026-10-12.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the completed shipment-record aggregation."
      },
      "evidence": {
        "text": "TimeoutError totals: dispatch-api 1,947; customer-tracking 181; label-scheduler 56; overall 2,184."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous query covering regional and private infrastructure was accepted but no completed result was provided, so concentration outside customer-facing systems remains unverified.",
        "gap_reason": "other"
      }
    ]
  }
}
```