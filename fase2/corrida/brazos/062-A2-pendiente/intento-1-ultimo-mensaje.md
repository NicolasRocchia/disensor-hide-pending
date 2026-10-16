Yes. Northbridge Cell N-4 accounted for 148 of 178 affected jobs—about 83%. The other cells were Río Seco R-2 with 21 jobs and Harbor Point H-1 with 9.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events_aggregate",
      "severity": "info",
      "title": "Stockouts concentrated in Northbridge N-4",
      "description": "Northbridge Cell N-4 represented approximately 83% of jobs affected by servo-motor stockouts.",
      "location": "2026-10-12 production-equipment QC events",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the aggregation result: 148 of 178 distinct affected jobs."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, execution, or escalation issues remain for this production-equipment comparison."
  }
}
```