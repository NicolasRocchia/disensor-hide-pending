Yes. Northbridge recorded 518 of 779 SealIntegrityFault events across primary and secondary lines—about 66.5%, so roughly two-thirds occurred there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "telemetry-review",
      "severity": "info",
      "title": "Northbridge held the majority",
      "description": "Northbridge accounted for 518 of 779 SealIntegrityFault events across primary and secondary production lines.",
      "final_state": "refuted_verifiable",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied telemetry aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "SealIntegrityFault — 779; Northbridge: 518; Riverside: 158; Westhaven: 103."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains within the supplied telemetry scope and aggregation."
  }
}
```