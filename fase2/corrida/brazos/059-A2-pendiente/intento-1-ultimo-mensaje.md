Yes. Cordoba Foundry Line F3 accounted for 1,746 of the 2,184 wafer-transfer alignment failures—about 80%. No other line was close: F1 had 286 and Rosario R2 had 152. The broader query including advanced-packaging facilities was still pending, so this conclusion applies to the completed external-services dataset.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate",
      "severity": "info",
      "title": "Line F3 dominated wafer-related delays",
      "description": "Cordoba Foundry Line F3 accounted for 1,746 of 2,184 wafer-transfer alignment failures, approximately 80 percent.",
      "location": "Cordoba Foundry / Line F3",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the completed external-services QC aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "Wafer transfer alignment failure: 2,184 jobs; Cordoba Foundry Line F3: 1,746 jobs."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The expanded aggregation including advanced-packaging facilities was accepted but no result was returned, so its distribution could not be evaluated.",
        "gap_reason": "other"
      }
    ]
  }
}
```