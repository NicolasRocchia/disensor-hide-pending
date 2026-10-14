Yes. Northbridge accounted for 421 of 612 SealIntegrityFault events—about 68.8%—so a clear majority within the three-facility primary-line dataset for October 12, 2026.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "telemetry.aggregate_defects",
      "severity": "info",
      "title": "Most seal faults occurred at Northbridge",
      "description": "Northbridge recorded 421 of the 612 SealIntegrityFault events, representing approximately 68.8% of the total.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Checked against the supplied telemetry aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "SealIntegrityFault: 612 total events; Northbridge: 421 events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified conclusions remain for this calculation."
  }
}
```