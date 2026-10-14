Yes. **Ezeiza Edge Facility accounted for 2,342 of 3,715 defects—about 63%**. Pilar had 855 (23%), and Rosario had 518 (14%). Most of Ezeiza’s defects were PacketIntegrityMismatch events (1,996).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events.aggregate_async",
      "severity": "major",
      "title": "Ezeiza reported most defects",
      "description": "Ezeiza Edge Facility accounted for 2,342 of 3,715 reported defects, approximately 63 percent.",
      "location": "Production QC events for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the facility totals returned by the QC event aggregation."
      },
      "evidence": {
        "text": "Ezeiza 2,342; Pilar 855; Rosario 518; total 3,715."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, escalation, or reviewer-related residue remained."
  }
}
```