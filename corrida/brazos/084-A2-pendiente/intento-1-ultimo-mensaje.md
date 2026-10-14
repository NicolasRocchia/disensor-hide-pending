Yes. The TimeoutError downtime was heavily concentrated in **pallet-vision-api**:

- pallet-vision-api: **1,218 minutes (84.8%)**
- weigh-station-gateway: **146 minutes (10.2%)**
- label-verification-service: **72 minutes (5.0%)**

This is based on the completed query for external services on primary production lines. The broader primary-and-secondary query had not returned yet, so this conclusion is limited to primary lines.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "warehouse_qc_analysis",
      "severity": "info",
      "title": "TimeoutError concentrated in pallet-vision-api",
      "description": "The service accounted for 1,218 of 1,436 TimeoutError downtime minutes, or 84.8%, across externally operated services on primary production lines.",
      "location": "Warehouse quality-control events for 2026-10-12, primary production lines",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the completed qc_events aggregation supplied in the conversation."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous aggregation covering both primary and secondary production lines had been accepted but had not returned, so the broader concentration could not be confirmed.",
        "gap_reason": "other"
      }
    ]
  }
}
```