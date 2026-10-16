Yes. Across primary and secondary lines, **pallet-vision-api accounted for 1,602 of 1,972 TimeoutError downtime minutes (81.2%)** and 2,559 of 3,127 events (81.8%). The remaining downtime was split between weigh-station-gateway (243 minutes) and label-verification-service (127 minutes).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate_async",
      "severity": "major",
      "title": "TimeoutError concentrated in pallet-vision-api",
      "description": "The service accounted for 81.2% of TimeoutError downtime across primary and secondary production lines.",
      "location": "External services on primary and secondary production lines, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed QC aggregation: 1,602 of 1,972 TimeoutError downtime minutes."
      },
      "fix_verification": {
        "type": "pending_in_diff_gate",
        "reference": "Analytical finding only; no corrective change was applied."
      },
      "evidence": {
        "text": "pallet-vision-api: 2,559 TimeoutError events and 1,602 downtime minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical questions or unverified execution gaps remained in this review."
  }
}
```