Yes. At Córdoba Assembly, there were 493 of 650 SD-48 stockout events—75.8%. Rosario had 101 (15.5%) and Pilar had 56 (8.6%). Thus, roughly three-quarters were concentrated at Córdoba.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_review",
      "severity": "info",
      "title": "SD-48 stockouts concentrated at Córdoba",
      "description": "Córdoba Assembly accounted for 493 of 650 SD-48 stockout events, or 75.8 percent.",
      "location": "Inventory logs for 2026-10-12, all equipment scopes",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory aggregation grouped by component and facility."
      },
      "evidence": {
        "text": "servo-drive SD-48: 650; Cordoba Assembly: 493; Rosario Robotics: 101; Pilar Integration: 56"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions, execution gaps, or interpretive disputes remain from this analysis."
  }
}
```