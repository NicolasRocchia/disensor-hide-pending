Yes. Cambridge Lab accounted for 214 of 271 reported peristaltic pump tubing stockouts—about 79%. Rosario Analytics and Cordoba BioWorks accounted for 39 and 18, respectively.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_records",
      "severity": "info",
      "title": "Cambridge Lab dominated tubing stockouts",
      "description": "Cambridge Lab accounted for approximately 79% of reported peristaltic pump tubing stockouts.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied stockout aggregation: Cambridge Lab recorded 214 of 271 events."
      },
      "evidence": {
        "text": "Cambridge Lab: 214; component total: 271"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions, execution gaps, or interpretive disputes remain for this calculation."
  }
}
```