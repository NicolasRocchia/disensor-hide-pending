Yes. Including maintenance-only equipment, Rosario Assembly reported **1,984 of 3,671 defects (54.0%)**, so it accounted for a majority. Customer-facing systems alone show the same result: **1,782 of 3,184 (56.0%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_jobs",
      "severity": "info",
      "title": "Rosario reported most shortages",
      "description": "Rosario Assembly accounted for 1,984 of 3,671 component-shortage defects when maintenance-only equipment was included.",
      "location": "qc_jobs.aggregate_failures for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Summed Rosario counts across all four components and compared the result with the reported total."
      },
      "evidence": {
        "text": "Rosario Assembly: 1,533 SE-42, 245 PSK-8, 108 VI-16, and 98 TC-9 reports; total 1,984 of 3,671."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified analytical gaps remain for this calculation."
  }
}
```