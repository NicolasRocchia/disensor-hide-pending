Not yet confirmed across **all** production lines—the all-lines query was accepted but no result was returned. In the available standard-pool data, line-alpha caused **1,947 of 2,184** pallet label mismatches (**89.1%**), so it clearly accounted for most among the reported lines.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "All-lines result remains pending",
      "description": "Line-alpha accounted for 89.1% of reported pallet label mismatch failures, but the asynchronous query covering all production lines has no returned result, so the broader conclusion cannot yet be confirmed.",
      "location": "warehouse_failures.aggregate_async request wfagg_7Q2M91KX"
    }
  ]
}
```