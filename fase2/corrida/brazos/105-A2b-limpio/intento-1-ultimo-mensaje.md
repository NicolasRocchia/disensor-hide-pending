Yes. Across primary and secondary lines, **inventory-sync-gateway accounted for 2,359 of 2,683 TimeoutErrors (87.9%)**. The remainder came from supplier-stock-adapter (245; 9.1%) and parts-reservation-scheduler (79; 2.9%). The problem was therefore strongly concentrated in inventory-sync-gateway.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in inventory-sync-gateway",
      "description": "Inventory-sync-gateway produced 2,359 of 2,683 TimeoutErrors (87.9%) across primary and secondary production lines on 2026-10-12.",
      "location": "inventory-sync-gateway; primary and secondary production lines"
    }
  ]
}
```