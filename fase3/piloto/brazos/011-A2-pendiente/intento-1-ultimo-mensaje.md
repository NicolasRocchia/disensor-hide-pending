Yes. Cell-culture-2 accounted for 74 of 96 servo-motor stockouts—about 77%. The remaining 22 occurred in assay-prep-1 (15) and centrifuge-build-3 (7).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_failures.aggregate",
      "severity": "info",
      "title": "Servo-motor stockouts were concentrated",
      "description": "Cell-culture-2 generated approximately 77% of all servo-motor assembly stockout events.",
      "location": "2026-10-12 non-reserved inventory",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory aggregation results."
      },
      "evidence": {
        "text": "cell-culture-2 recorded 74 of 96 servo-motor assembly stockout events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains in this conclusion based on the supplied inventory aggregation."
  }
}
```