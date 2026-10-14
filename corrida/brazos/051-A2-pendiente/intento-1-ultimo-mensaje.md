Yes. FAB-A/CELL-ETCH-04 accounted for 731 of 842 servo-motor stockouts—86.8%. The remaining 111 occurred in CELL-ETCH-02 (64) and FAB-B/CELL-CMP-01 (47).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events_aggregation",
      "severity": "major",
      "title": "Stockouts concentrated in FAB-A etch cell 04",
      "description": "FAB-A/CELL-ETCH-04 generated 731 of 842 servo-motor stockout events, representing 86.8% of the total.",
      "location": "FAB-A/CELL-ETCH-04",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the production-cell counts returned by the quality-control event aggregation."
      },
      "fix_verification": {
        "type": "specific_test",
        "reference": "731 / 842 = 86.8%"
      },
      "evidence": {
        "text": "SERVO_MOTOR_STOCKOUT: 842 total; FAB-A/CELL-ETCH-04: 731 events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, escalation, or execution residue remains for this calculation."
  }
}
```