Yes. FAB-A/CELL-ETCH-04 recorded 731 of the 842 servo-motor stockouts—about 86.8%. The other two cells accounted for only 111 combined, so the stockouts were strongly concentrated in that one cell.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events_reviewer",
      "severity": "major",
      "title": "Stockouts concentrated in etch cell 04",
      "description": "FAB-A/CELL-ETCH-04 accounted for 731 of 842 servo-motor stockout events, approximately 86.8 percent.",
      "location": "FAB-A/CELL-ETCH-04",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the QC event aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "SERVO_MOTOR_STOCKOUT: 842 total; FAB-A/CELL-ETCH-04: 731."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains from this production-cell concentration assessment."
  }
}
```