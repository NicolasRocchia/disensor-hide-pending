Yes. **FAB-A/CELL-ETCH-04 recorded 731 stockouts**:

- 76.1% of all 960 stockouts across wafer fabs and advanced packaging.
- 86.8% of the 842 events initially reported on primary wafer-fab lines.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_event_analysis",
      "severity": "major",
      "title": "Stockouts concentrated in FAB-A etch cell 04",
      "description": "FAB-A/CELL-ETCH-04 accounted for 731 of 960 servo-motor stockout events across all reviewed production lines.",
      "location": "FAB-A/CELL-ETCH-04",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the provided QC aggregation results for 2026-10-12."
      },
      "evidence": {
        "text": "FAB-A/CELL-ETCH-04 recorded 731 of 960 servo-motor stockout events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains from the supplied production-event aggregates."
  }
}
```