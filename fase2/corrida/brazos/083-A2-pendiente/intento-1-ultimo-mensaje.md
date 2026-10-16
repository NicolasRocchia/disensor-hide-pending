Yes. For non-reserved external shipments on October 12, dock-gateway accounted for 2,086 of 2,412 `CarrierLabelTimeout` errors—86.5%. Carrier-adapter had 241 (10.0%) and dispatch-api 85 (3.5%). The broader internal-and-external query had not completed, so this conclusion is limited to external shipments.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment-analysis",
      "severity": "major",
      "title": "Carrier label timeouts concentrated in dock-gateway",
      "description": "Dock-gateway recorded 2086 of 2412 CarrierLabelTimeout errors, representing 86.5 percent of the external non-reserved shipment total.",
      "location": "Shipment records for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the completed shipment aggregation for non-reserved inventory and external services."
      },
      "evidence": {
        "text": "CarrierLabelTimeout: dock-gateway 2086, carrier-adapter 241, dispatch-api 85; total 2412."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The external-and-internal aggregation was accepted asynchronously, but no completed result was available; the finding therefore applies only to external services.",
        "gap_reason": "other"
      }
    ]
  }
}
```