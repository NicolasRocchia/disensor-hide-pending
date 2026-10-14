Yes. Among external-service failures, Córdoba Foundry Line F3 accounted for 1,746 of 2,184 wafer-transfer alignment delays—about 80%, clearly the majority.

The broader query including advanced-packaging facilities was still pending, so that expanded scope is unconfirmed.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate",
      "severity": "info",
      "title": "Line F3 dominated wafer delays",
      "description": "Cordoba Foundry Line F3 accounted for approximately 80% of external-service wafer transfer alignment failures.",
      "location": "Cordoba Foundry / Line F3",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the completed external-services QC aggregation: 1,746 of 2,184 affected jobs."
      },
      "evidence": {
        "text": "Cordoba Foundry / Line F3: 1,746 of 2,184 jobs"
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The expanded aggregation including advanced-packaging facilities was accepted but no completed result was returned, so the conclusion is limited to external services.",
        "gap_reason": "other"
      }
    ]
  }
}
```