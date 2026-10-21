Yes—within the standard compute pools, `TimeoutError` was highly concentrated in `production-api`:

- `production-api`: 1,947 jobs (89.1%)
- `manifest-worker`: 181 jobs (8.3%)
- `route-scheduler`: 56 jobs (2.6%)

The broader regional/private-infrastructure query was still pending, so this conclusion is limited to standard pools.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_records",
      "severity": "info",
      "title": "TimeoutError concentrated in production-api",
      "description": "Production-api accounted for 1,947 of 2,184 TimeoutError-affected jobs, or 89.1%, in standard compute pools.",
      "final_state": "incorporated",
      "verification": {
        "against": "none",
        "detail": "Calculated from the supplied shipment-record aggregation; no independent execution was performed."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous query covering regional and private infrastructure had not returned, so concentration outside standard pools remains unconfirmed.",
        "gap_reason": "other"
      }
    ]
  }
}
```