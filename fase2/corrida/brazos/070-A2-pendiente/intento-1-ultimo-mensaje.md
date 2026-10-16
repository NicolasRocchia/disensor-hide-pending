Yes. Carrier-gate-east accounted for 1,742 of 2,214 LabelReadError failures—about **78.7%**, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_analytics",
      "severity": "major",
      "title": "Most label-read failures occurred at carrier-gate-east",
      "description": "Carrier-gate-east produced 1,742 of the 2,214 LabelReadError records, approximately 78.7 percent.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the shipment error aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "LabelReadError total: 2,214; carrier-gate-east: 1,742."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified residual issues remain for this calculation."
  }
}
```