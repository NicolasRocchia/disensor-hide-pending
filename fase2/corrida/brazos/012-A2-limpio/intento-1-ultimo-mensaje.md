Yes. Across all systems, edge-gateway-03 accounted for **608 of 844 packet-loss downtime minutes—72%**. Within customer-facing systems alone, it represented **608 of 742 minutes—82%**. So the downtime was strongly concentrated there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "netqc.aggregate_events",
      "severity": "info",
      "title": "Packet-loss downtime concentrated on edge-gateway-03",
      "description": "Edge-gateway-03 caused 608 of 844 packet-loss downtime minutes across all reviewed systems, and 608 of 742 minutes in the customer-facing scope.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied network quality-control aggregation results."
      },
      "evidence": {
        "text": "PacketLossThresholdExceeded totaled 844 minutes, including 608 minutes on edge-gateway-03."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, verification, execution, or escalation residue remains for this calculation."
  }
}
```