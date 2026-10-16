Yes. Servo-motor stockouts were heavily concentrated in **CELL-F12**:

- Customer-facing scope: **78 of 96 events (81.3%)**
- Including internal services: **94 of 118 events (79.7%)**

So roughly four out of every five servo-motor stockouts occurred in CELL-F12.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory-analysis",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in CELL-F12",
      "description": "CELL-F12 accounted for 78 of 96 customer-facing events and 94 of 118 events when internal services were included.",
      "location": "FAB-NORTE/CELL-F12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the manufacturing stockout aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "CELL-F12 recorded 78 of 96 customer-facing servo-motor stockouts and 94 of 118 under the expanded scope."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical questions or unverified execution gaps remained after reviewing both reported system scopes."
  }
}
```