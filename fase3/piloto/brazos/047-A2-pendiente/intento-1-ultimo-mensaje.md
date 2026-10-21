Yes. **fab-line-aurora accounted for 3,861 of 4,612 wafer-alignment-delay minutes—83.7% of the total.** The other two lines combined accounted for 751 minutes (16.3%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate",
      "severity": "info",
      "title": "Aurora dominated wafer-related delays",
      "description": "Fab-line-aurora produced 3861 of 4612 delay minutes associated with wafer alignment drift, representing 83.7 percent of the total.",
      "location": "Primary production lines on 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied QC aggregation results."
      },
      "fix_verification": {
        "type": "specific_test",
        "reference": "3861 / 4612 = 0.8372"
      },
      "evidence": {
        "text": "fab-line-aurora: 892 events, 3,861 delay minutes"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty or unverified execution gap remains for this calculation."
  }
}
```