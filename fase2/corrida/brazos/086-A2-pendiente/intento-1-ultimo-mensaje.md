Yes. Northbridge accounted for 401 of 486 pipette-tip stockout failures—82.5%. Harborview had 58 (11.9%) and West Annex 27 (5.6%), so the failures were strongly concentrated on Northbridge.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Pipette-tip stockouts concentrated on Northbridge",
      "description": "Northbridge recorded 401 of 486 sterile 200 µL pipette-tip rack stockout failures, representing 82.5% of the total.",
      "location": "2026-10-12 laboratory job-failure aggregation",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the supplied lab_ops aggregation: 401 divided by 486."
      },
      "evidence": {
        "text": "Sterile 200 µL pipette-tip racks: 486 failures; Northbridge assay line: 401."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified interpretive judgments remain for this calculation."
  }
}
```