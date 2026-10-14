Yes. Harbor Point accounted for **755 of 1,072 SFP-25G stockout events (70.4%)** across all facilities—about **4.7×** Northgate’s 159 events. The concentration was even higher on primary lines: **684 of 903 events (75.7%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events",
      "severity": "info",
      "title": "SFP-25G stockouts concentrated at Harbor Point",
      "description": "Harbor Point generated 755 of 1,072 SFP-25G transceiver stockout events, representing 70.4% of the total.",
      "location": "Inventory events for 2026-10-12 across all facilities and production lines",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory_events aggregate result."
      },
      "evidence": {
        "text": "Harbor Point: 755 events; all facilities: 1,072 events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, execution, or escalation residue remains."
  }
}
```