Yes. For non-reserved external shipments on October 12, dock-gateway accounted for 2,086 of 2,412 `CarrierLabelTimeout` errors—about **86.5%**. The remaining 13.5% came from carrier-adapter (241) and dispatch-api (85), so the problem was strongly concentrated in dock-gateway.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Carrier label timeouts concentrated in dock-gateway",
      "description": "dock-gateway recorded 2,086 of 2,412 CarrierLabelTimeout errors (86.5%) in non-reserved external shipments on 2026-10-12."
    }
  ]
}
```