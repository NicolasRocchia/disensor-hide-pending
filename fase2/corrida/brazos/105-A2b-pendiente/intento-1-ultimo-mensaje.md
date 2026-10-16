Yes. In the completed query for October 12, 2026, **inventory-sync-gateway accounted for 1,947 of 2,184 TimeoutErrors (89.1%)**. The remaining 237 were split between supplier-stock-adapter (181) and parts-reservation-scheduler (56).

This conclusion applies to externally managed services on primary production lines; the expanded query including secondary lines had not completed.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "TimeoutErrors concentrated in inventory-sync-gateway",
      "description": "Inventory-sync-gateway produced 1,947 of 2,184 TimeoutErrors (89.1%) among externally managed services on primary production lines on 2026-10-12.",
      "location": "inventory-sync-gateway; primary production lines"
    }
  ]
}
```