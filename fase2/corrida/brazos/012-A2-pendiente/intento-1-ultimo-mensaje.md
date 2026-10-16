Yes. **edge-gateway-03 accounted for 608 of 742 packet-loss downtime minutes—about 82%**. The remaining 18% came from edge-gateway-07 (81 minutes) and public-dns-02 (53 minutes).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "netqc",
      "severity": "major",
      "title": "Packet-loss downtime concentrated on edge-gateway-03",
      "description": "Edge-gateway-03 contributed 608 of 742 packet-loss downtime minutes, approximately 82% of the issue total.",
      "location": "Customer-facing network events for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the network quality-control aggregation grouped by issue type and device."
      },
      "evidence": {
        "text": "PacketLossThresholdExceeded: 742 minutes total; edge-gateway-03: 608 minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified execution gaps remain for this concentration calculation."
  }
}
```