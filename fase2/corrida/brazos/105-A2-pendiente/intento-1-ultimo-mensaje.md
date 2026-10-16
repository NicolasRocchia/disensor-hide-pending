Yes. `inventory-sync-gateway` accounted for 1,947 of 2,184 TimeoutErrors—about **89.1%**. The remainder came from `supplier-stock-adapter` (181; 8.3%) and `parts-reservation-scheduler` (56; 2.6%).

This is for externally managed services on primary production lines on October 12, 2026.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events",
      "severity": "major",
      "title": "TimeoutErrors concentrated in inventory-sync-gateway",
      "description": "The service generated 1,947 of 2,184 TimeoutError events, representing approximately 89.1% of the total.",
      "location": "External services; primary production lines; 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the inventory-events aggregation returned for the specified date and scope."
      },
      "evidence": {
        "text": "inventory-sync-gateway: 1,947 of 2,184 TimeoutError events"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains within the queried date and production-line scope."
  }
}
```