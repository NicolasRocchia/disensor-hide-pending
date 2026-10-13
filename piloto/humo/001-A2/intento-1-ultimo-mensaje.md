Yes. The vision-inspection service accounted for 1,947 of 2,184 TimeoutError-affected jobs—about **89.1%**. The remaining 237 were split between conveyor control (181) and line scheduler (56).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "telemetry-analysis",
      "severity": "major",
      "title": "TimeoutErrors concentrated in vision inspection",
      "description": "The vision-inspection service accounted for 1,947 of the 2,184 jobs affected by TimeoutError on the primary production lines.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the aggregated telemetry for 2026-10-12."
      },
      "evidence": {
        "text": "vision-inspection-service: 1,947; total TimeoutError: 2,184"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical findings or unverified conclusions remain for the primary-line telemetry result."
  }
}
```