Yes. In non-reserved inventory, **litho-dispatch accounted for 1,926 of 2,184 ReticleSyncTimeout events (88.2%)**. Wafer-routing had 174 (8.0%), and mask-catalog had 84 (3.8%). The broader query including reserved compute capacity was still pending, so this concentration is not yet confirmed across all inventory.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate",
      "severity": "info",
      "title": "ReticleSyncTimeout concentrated in litho-dispatch",
      "description": "Litho-dispatch produced 1926 of 2184 ReticleSyncTimeout events in non-reserved inventory, representing 88.2 percent.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the inventory aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "ReticleSyncTimeout: 2184; litho-dispatch: 1926; wafer-routing: 174; mask-catalog: 84."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous aggregation including reserved compute capacity had not returned, so the result is limited to non-reserved inventory.",
        "gap_reason": "other"
      }
    ]
  }
}
```