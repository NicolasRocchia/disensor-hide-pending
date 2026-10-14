Yes. Northbridge accounted for **401 of 486 customer-facing pipette-tip stockout failures (82.5%)**. Even including automated warehouse inventory, it represented **401 of 577 failures (69.5%)**, so the failures were clearly concentrated there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Northbridge dominated pipette-tip stockouts",
      "description": "Northbridge recorded 401 of 486 customer-facing failures and 401 of 577 failures when warehouse inventory was included.",
      "location": "Northbridge assay line",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the supplied aggregated laboratory operations results."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, execution, or escalation residue remains."
  }
}
```