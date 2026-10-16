Yes. FAB-L3 accounted for most WaferAlignTimeout delays:

- Standard compute: 143 of 184 affected jobs (77.7%)
- Including maintenance-only equipment: 151 of 197 (76.6%)

So the concentration on FAB-L3 remains clear under either scope.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "telemetry-analysis",
      "severity": "major",
      "title": "Wafer delays concentrated on FAB-L3",
      "description": "FAB-L3 accounted for more than three-quarters of jobs affected by WaferAlignTimeout.",
      "location": "FAB-L3 telemetry for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against aggregated equipment telemetry for standard-compute and maintenance-only scopes."
      },
      "evidence": {
        "text": "FAB-L3 affected 143 of 184 standard-compute jobs and 151 of 197 jobs when maintenance-only equipment was included."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved qualification, verification, or interpretation remained after comparing both reported equipment scopes."
  }
}
```