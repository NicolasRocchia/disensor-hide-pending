Yes. Cell-alpha-04 accounted for 681 of 812 affected jobs—about 84%. The remaining 131 were split between cell-alpha-02 (79) and cell-beta-01 (52).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory-analysis",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in cell-alpha-04",
      "description": "Cell-alpha-04 represented approximately 84% of jobs affected by servo-motor stockouts.",
      "location": "primary_production_lines/cell-alpha-04",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the inventory event aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "cell-alpha-04 affected 681 of the 812 distinct jobs impacted by servo-motor stockouts."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains for the production-cell concentration finding."
  }
}
```