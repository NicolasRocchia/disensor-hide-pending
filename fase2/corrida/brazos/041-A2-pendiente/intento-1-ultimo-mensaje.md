Yes. Northbridge accounted for 421 of 612 SealIntegrityFault events—about 68.8%, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "telemetry.aggregate_defects",
      "severity": "info",
      "title": "Northbridge recorded the majority",
      "description": "Northbridge contributed 421 of 612 SealIntegrityFault events.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied telemetry aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "SealIntegrityFault — 612; Northbridge: 421"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains in this calculation based on the supplied telemetry results."
  }
}
```