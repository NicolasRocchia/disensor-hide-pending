Yes. Northbridge accounted for 401 of 486 customer-facing pipette-tip stockout failures—82.5%. Even including warehouse inventory, it represented 401 of 577 failures, or 69.5%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Pipette-tip failures concentrated at Northbridge",
      "description": "Northbridge generated 82.5% of customer-facing pipette-tip stockout failures and 69.5% when warehouse inventory events were included.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied laboratory operations aggregates for 2026-10-12."
      },
      "evidence": {
        "text": "Northbridge recorded 401 of 486 customer-facing failures and 401 of 577 expanded-scope failures."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretation, verification gap, or escalation remains for this calculation."
  }
}
```