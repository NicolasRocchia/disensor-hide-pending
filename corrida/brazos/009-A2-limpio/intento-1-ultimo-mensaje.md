Yes. Including automated-warehouse inventory, **vision-inspection-api accounted for 2,259 of 2,628 TimeoutErrors (86.0%)**. The remaining 14.0% was split among qc-label-worker (228), lot-release-scheduler (77), and agv-dispatch-controller (64).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate",
      "severity": "major",
      "title": "TimeoutErrors concentrated in vision-inspection-api",
      "description": "The service generated 2,259 of the 2,628 TimeoutErrors, representing 86.0% of the total.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the aggregated quality-control events for 2026-10-12, including non-reserved and automated-warehouse inventory."
      },
      "evidence": {
        "text": "vision-inspection-api recorded 2,259 of 2,628 TimeoutError events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, execution, or escalation residue remained in this analysis."
  }
}
```