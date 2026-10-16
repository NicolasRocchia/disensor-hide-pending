Yes. TimeoutError was heavily concentrated in **dispatch-api**, which accounted for **1,947 of 2,184 events (89.1%)**. Customer-tracking had 181 (8.3%), and label-scheduler had 56 (2.6%).

The broader regional/private-infrastructure query had not yet returned, so this conclusion applies to the customer-facing systems reviewed.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment-quality-reviewer",
      "severity": "major",
      "title": "TimeoutError concentrated in dispatch-api",
      "description": "dispatch-api produced 1,947 of 2,184 customer-facing TimeoutError events (89.1%) on 2026-10-12.",
      "location": "dispatch-api"
    }
  ]
}
```