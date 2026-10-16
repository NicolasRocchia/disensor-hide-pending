Yes. North Materials Lab’s Line N-W2 accounted for 37 of 71 wafer-related delay events—52.1%, a narrow majority. All other lines combined accounted for 34 events. This rollup includes reserved inventory and compute capacity across all four facilities.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "lab_ops",
      "severity": "info",
      "title": "Line N-W2 caused most wafer-related delays",
      "description": "North Materials Lab Line N-W2 accounted for 37 of 71 wafer-related delay events, or 52.1%.",
      "location": "North Materials Lab / Line N-W2",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the lab_ops aggregate_component_delays result for 2026-10-12."
      },
      "evidence": {
        "text": "Wafer-handler vacuum end effectors — North Materials Lab / Line N-W2: 37; delay_events_total=71."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, execution, escalation, or reviewer-related residue remains."
  }
}
```