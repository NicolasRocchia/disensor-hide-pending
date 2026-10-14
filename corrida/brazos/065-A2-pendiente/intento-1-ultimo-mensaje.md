Yes. In non-reserved inventory, Rosario accounted for 119 of 146 servo-motor SM-42 stockouts—about 81.5%. Córdoba had 18 and Santa Fe had 9. The broader automated-warehouse query had not yet returned, so this conclusion is limited to non-reserved inventory.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory-analysis",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in Rosario",
      "description": "Rosario recorded 119 of 146 non-reserved SM-42 stockout incidents, approximately 81.5 percent.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the inventory incident aggregation for 2026-10-12."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The automated-warehouse aggregation was accepted asynchronously but no completed result was available, so the conclusion covers only non-reserved inventory.",
        "gap_reason": "other"
      }
    ]
  }
}
```