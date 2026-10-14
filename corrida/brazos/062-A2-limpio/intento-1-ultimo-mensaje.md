Yes. Northbridge Cell N-4 accounted for 148 of 178 affected production jobs—about 83%. Even including internal services, it represented 148 of 191 jobs, or 77%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_events",
      "severity": "info",
      "title": "Stockouts concentrated in Cell N-4",
      "description": "Northbridge Cell N-4 accounted for 148 of 178 affected production jobs.",
      "location": "Northbridge / Cell N-4",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the QC event aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "Northbridge / Cell N-4: 148 of 178 production jobs affected."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty or unverified execution gap remained in this analysis."
  }
}
```