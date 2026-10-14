Yes. Phoenix had 853 of 1,092 25GbE NIC module stockouts—about **78.1%**, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_analysis",
      "severity": "info",
      "title": "Most NIC stockouts occurred at Phoenix",
      "description": "Phoenix recorded 853 of 1,092 25GbE NIC module stockout events, approximately 78.1%.",
      "location": "phoenix-integration",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the supplied aggregate_stockouts result for 2026-10-12."
      },
      "evidence": {
        "text": "25GbE NIC module: 1,092 total stockouts; phoenix-integration: 853."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretation, execution gap, or escalation remains for this calculation."
  }
}
```