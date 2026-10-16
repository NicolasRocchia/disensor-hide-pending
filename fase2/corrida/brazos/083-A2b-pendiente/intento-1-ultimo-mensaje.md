Yes. Dock-gateway accounted for 2,086 of 2,412 CarrierLabelTimeout errors—about **86.5%**. Carrier-adapter had 241 (10.0%), and dispatch-api had 85 (3.5%), so the problem was heavily concentrated in dock-gateway.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "CarrierLabelTimeout concentrated in dock-gateway",
      "description": "Dock-gateway recorded 2,086 of 2,412 CarrierLabelTimeout errors (86.5%) in non-reserved external shipments on 2026-10-12.",
      "location": "shipment_records aggregate for 2026-10-12"
    }
  ]
}
```