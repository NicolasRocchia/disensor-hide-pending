Yes. Cordoba Foundry’s Line F3 accounted for 1,746 of 2,535 wafer-related delayed jobs—about 68.9%, so it alone represented a clear majority. The next-largest line, F1, accounted for only 286 jobs.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events",
      "severity": "major",
      "title": "Line F3 caused most wafer-related delays",
      "description": "Cordoba Foundry Line F3 accounted for 1,746 of 2,535 affected jobs, approximately 68.9 percent.",
      "location": "Cordoba Foundry / Line F3",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied QC aggregation for external services and advanced packaging facilities."
      },
      "evidence": {
        "text": "Cordoba Foundry / Line F3: 1,746 of 2,535 distinct jobs affected."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretation, execution gap, or escalation remains for this calculation."
  }
}
```