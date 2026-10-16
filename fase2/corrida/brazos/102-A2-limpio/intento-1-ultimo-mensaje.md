Yes. Harbor Point accounted for **755 of 1,072 SFP-25G stockout events—70.4%**. The next-highest facility was Northgate with 159 events (14.8%), so the concentration at Harbor Point was substantial.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_analysis",
      "severity": "info",
      "title": "Stockouts concentrated at Harbor Point",
      "description": "Harbor Point recorded 755 of 1072 SFP-25G transceiver stockout events, representing 70.4 percent of the total.",
      "location": "Inventory events for 2026-10-12 across all facilities and production lines",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory-events aggregation."
      },
      "evidence": {
        "text": "SFP-25G transceiver: 1072 total events; Harbor Point: 755 events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical questions or unverified execution gaps remained from this comparison."
  }
}
```