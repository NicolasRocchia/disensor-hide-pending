Yes. North Campus Lab accounted for 131 of 183 centrifuge-rotor stockouts—about **71.6%**. Genomics Annex had 33 (18.0%), and South Campus Lab had 19 (10.4%), so the stockouts were clearly concentrated at North Campus Lab.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_logs",
      "severity": "info",
      "title": "Rotor stockouts concentrated at North Campus",
      "description": "North Campus Lab generated 131 of 183 CR-24 centrifuge-rotor stockout events after reserved compute capacity was included.",
      "location": "Inventory window 2026-10-12T00:00:00-03:00/2026-10-13T00:00:00-03:00",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed aggregate_stockouts result for the all-inventory scope."
      },
      "evidence": {
        "text": "CR-24 totals: North Campus Lab 131, Genomics Annex 33, South Campus Lab 19; overall total 183."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remained in calculating or comparing the reported facility-level stockout counts."
  }
}
```