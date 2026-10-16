Yes. `inventory-sync` accounted for **2,421 of 2,764 minutes (87.6%)** of TimeoutError downtime. The remainder was in `cell-replenisher` (257 minutes) and `allocation-scheduler` (86 minutes).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate",
      "severity": "major",
      "title": "TimeoutError concentrated in inventory-sync",
      "description": "Inventory-sync accounted for 87.6% of all TimeoutError downtime during the reported period.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory-events aggregation."
      },
      "evidence": {
        "text": "inventory-sync: 2,421 of 2,764 TimeoutError downtime minutes"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "The supplied aggregation fully supports this concentration calculation; no unresolved analytical residue remains."
  }
}
```