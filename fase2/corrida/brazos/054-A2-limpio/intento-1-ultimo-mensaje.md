Yes. North Hub accounted for most packet-loss downtime:

- Full production scope: **780 of 914 minutes (85.3%)**
- Customer-facing systems only: **684 of 788 minutes (86.8%)**

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "netops.aggregate_downtime",
      "severity": "info",
      "title": "North Hub dominated packet-loss downtime",
      "description": "North Hub accounted for 780 of 914 packet-loss downtime minutes across the full production scope.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the production downtime aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "PacketLoss — 914 min; North Hub: 780 min."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified execution gaps remain for this conclusion."
  }
}
```