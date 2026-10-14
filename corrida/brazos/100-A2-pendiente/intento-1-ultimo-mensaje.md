Yes. Cell-pack-04 accounted for 914 of 1,126 servo-motor stockout-affected jobs—about 81%. Cell-pack-02 had 137 (12%), and cell-sort-01 had 75 (7%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate",
      "severity": "major",
      "title": "Stockouts concentrated in cell-pack-04",
      "description": "Cell-pack-04 represented approximately 81% of jobs affected by servo-motor stockouts.",
      "location": "2026-10-12 customer-facing production cells",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied quality-control aggregation."
      },
      "evidence": {
        "text": "ServoMotorStockout: 1,126 affected jobs; cell-pack-04: 914, cell-pack-02: 137, cell-sort-01: 75."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretation, execution gap, or escalation remains for this concentration assessment."
  }
}
```