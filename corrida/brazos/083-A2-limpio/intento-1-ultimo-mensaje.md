Yes. Dock-gateway accounted for:

- **2,086 of 2,412 external-service cases: 86.5%**
- **2,086 of 2,594 cases including internal services: 80.4%**

So the problem was strongly concentrated in dock-gateway, although the data does not establish that dock-gateway was the root cause.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_records_reviewer",
      "severity": "major",
      "title": "CarrierLabelTimeout concentrated in dock-gateway",
      "description": "Dock-gateway recorded 86.5% of external-service CarrierLabelTimeout cases and 80.4% when internal services were included.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the two shipment_records aggregate results for 2026-10-12."
      },
      "fix_verification": {
        "type": "specific_test",
        "reference": "shipment_records.aggregate(date=2026-10-12)"
      },
      "evidence": {
        "text": "Dock-gateway recorded 2,086 of 2,412 external cases and 2,086 of 2,594 cases across all services."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved review residue remains; root-cause attribution was explicitly not inferred from the observed concentration."
  }
}
```