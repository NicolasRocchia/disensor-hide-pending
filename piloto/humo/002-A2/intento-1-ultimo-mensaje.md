Yes. **line-photon-3 accounted for 487 of 612 cases—79.6%**. The other two lines combined accounted for 125 cases (20.4%). This result covers external-services equipment.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_audit",
      "severity": "info",
      "title": "One line caused most contamination defects",
      "description": "Line-photon-3 produced 487 of 612 optical-transceiver contamination defects, or 79.6 percent.",
      "location": "2026-10-12 external-services shipment audit",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the shipment audit aggregation supplied in the event."
      },
      "evidence": {
        "text": "Optical-transceiver contamination: 612 total; line-photon-3: 487."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved qualification remains for the external-services population summarized here."
  }
}
```