Yes. Dock-gateway accounted for **2,086 of 2,412 CarrierLabelTimeout errors—86.5%**. Carrier-adapter had 241 (10.0%) and dispatch-api 85 (3.5%). So the problem was strongly concentrated in dock-gateway within the external-service data. The internal-inclusive query had not yet completed.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "CarrierLabelTimeout concentrated in dock-gateway",
      "description": "Dock-gateway recorded 2,086 of 2,412 CarrierLabelTimeout errors, representing 86.5% of cases in the completed external-service aggregation.",
      "location": "shipment_records aggregation for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated 2,086 divided by 2,412 from the returned shipment aggregation."
      },
      "evidence": {
        "text": "CarrierLabelTimeout: 2,412 total; dock-gateway: 2,086; carrier-adapter: 241; dispatch-api: 85."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The external-and-internal service aggregation was accepted asynchronously, but no completed result was available to confirm whether including internal services changes the distribution.",
        "gap_reason": "other"
      }
    ]
  }
}
```