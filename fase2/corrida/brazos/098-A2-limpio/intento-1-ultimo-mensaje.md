Yes. Of 650 SD-48 stockout events across the full inventory scope, 493 occurred at Cordoba Assembly—75.8%. Rosario Robotics had 101 (15.5%), and Pilar Integration had 56 (8.6%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_logs",
      "severity": "info",
      "title": "SD-48 stockouts concentrated at Cordoba",
      "description": "Cordoba Assembly accounted for 493 of 650 SD-48 stockout events, or 75.8%.",
      "location": "Robotics factory inventory logs for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "repository",
        "detail": "Verified against the supplied aggregate inventory-log result."
      },
      "evidence": {
        "text": "Cordoba Assembly: 493; Rosario Robotics: 101; Pilar Integration: 56."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, execution, or escalation residue remains."
  }
}
```