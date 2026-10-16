Yes. Fab Line S4 accounted for 290 of 399 wafer-related stockout events on October 12—about 72.7%—so it represented a clear majority. This uses stockout events as the measure of delays; it does not measure delay duration.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_records",
      "severity": "info",
      "title": "Fab Line S4 dominated wafer-related stockouts",
      "description": "Fab Line S4 recorded 271 wafer-carrier assembly stockouts and 19 wafer-level packaging substrate stockouts, totaling 290 of 399 wafer-related events.",
      "location": "Shipment records for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied shipment-record aggregation for standard compute pools and advanced packaging facilities."
      },
      "evidence": {
        "text": "Fab Line S4 accounted for 290 of 399 wafer-related stockout events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved findings or execution gaps remained after reviewing the supplied shipment aggregation."
  }
}
```