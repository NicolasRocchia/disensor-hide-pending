Yes. TimeoutError was heavily concentrated in **inventory-sync**:

- Including automated warehouse inventory: **2,739 of 3,288 minutes (83.3%)**
- Non-reserved inventory alone: **2,421 of 2,764 minutes (87.6%)**

No other service exceeded 298 minutes, so inventory-sync was clearly the main source.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate",
      "severity": "major",
      "title": "TimeoutError concentrated in inventory-sync",
      "description": "Inventory-sync accounted for 2739 of 3288 TimeoutError downtime minutes across the combined inventory scope.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the inventory event aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "TimeoutError: 3,288 total downtime minutes; inventory-sync: 2,739 minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved ambiguity or execution gap remains in this concentration assessment."
  }
}
```