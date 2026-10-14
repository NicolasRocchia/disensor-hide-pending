Yes. **edge-gateway-03 accounted for 608 of 742 packet-loss downtime minutes—81.9%**. The remaining 134 minutes were split between edge-gateway-07 (81) and public-dns-02 (53).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "netqc.aggregate_events",
      "severity": "info",
      "title": "Packet-loss downtime concentrated on edge-gateway-03",
      "description": "edge-gateway-03 contributed 608 of 742 packet-loss downtime minutes, or 81.9%.",
      "location": "Customer-facing systems, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated directly from the supplied network quality-control aggregation: 608 / 742."
      },
      "evidence": {
        "text": "PacketLossThresholdExceeded: 742 minutes total; edge-gateway-03: 608 minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains within the supplied customer-facing network event data."
  }
}
```