Yes. In customer-facing systems, **cell-pack-04 accounted for 781 of 934 servo-motor stockout failures—83.6%**. The remaining failures were in cell-pack-02 (96) and cell-assembly-07 (57).

Including maintenance-only systems, cell-pack-04 still represented **823 of 1,031 failures—79.8%**. So the stockouts were strongly concentrated in that production cell.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_ops",
      "severity": "major",
      "title": "Stockouts concentrated in cell-pack-04",
      "description": "Cell-pack-04 accounted for 781 of 934 customer-facing jobs affected by servo-motor stockouts, or 83.6 percent.",
      "location": "robotics-west/cell-pack-04",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the inventory_ops aggregate for 2026-10-12."
      },
      "evidence": {
        "text": "ServoMotorStockout: cell-pack-04 affected 781 of 934 customer-facing jobs."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved ambiguity or unverified execution gap remained in this concentration analysis."
  }
}
```