Yes. Ezeiza Compute Depot accounted for 49 of 68 HBM3 accelerator-module stockouts—about 72%—so a clear majority were concentrated there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_records",
      "severity": "info",
      "title": "HBM3 stockouts concentrated at Ezeiza",
      "description": "Ezeiza Compute Depot recorded 49 of the 68 HBM3 accelerator-module stockouts, representing approximately 72 percent.",
      "location": "External-services shipment records for 2026-10-12",
      "final_state": "refuted_verifiable",
      "verification": {
        "against": "execution",
        "detail": "Verified against the reported shipment-record aggregation grouped by component and facility."
      },
      "evidence": {
        "text": "HBM3 accelerator module: 68 total out-of-stock events; Ezeiza Compute Depot: 49."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, execution, escalation, or reviewer-related residue remains for this calculation."
  }
}
```