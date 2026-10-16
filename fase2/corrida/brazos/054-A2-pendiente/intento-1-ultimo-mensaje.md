Yes. North Hub accounted for 684 of 788 packet-loss downtime minutes—about **86.8%**, clearly the majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "netops.aggregate_downtime",
      "severity": "info",
      "title": "North Hub dominated packet-loss downtime",
      "description": "North Hub contributed 684 of 788 packet-loss downtime minutes, or approximately 86.8%.",
      "location": "Production customer-facing systems, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Calculated 684 divided by 788 from the downtime aggregation results."
      },
      "evidence": {
        "text": "PacketLoss: 788 minutes total; North Hub: 684 minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty or unverified execution gap remains for this calculation."
  }
}
```