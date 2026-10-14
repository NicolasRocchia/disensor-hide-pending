Yes. `inventory-sync` accounted for **2,421 of 2,764 minutes (87.6%)** of TimeoutError downtime. The remainder was split between `cell-replenisher` (257 minutes, 9.3%) and `allocation-scheduler` (86 minutes, 3.1%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate",
      "severity": "major",
      "title": "TimeoutError concentrated in inventory-sync",
      "description": "Inventory-sync caused 2,421 of 2,764 TimeoutError downtime minutes, representing 87.6% of the total.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the inventory event aggregation for 2026-10-12 in America/Buenos_Aires."
      },
      "evidence": {
        "text": "inventory-sync: 2,421 minutes and 1,947 events; TimeoutError total: 2,764 minutes and 2,184 events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains within the supplied non-reserved inventory event data."
  }
}
```