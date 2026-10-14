Yes. After internal services were included, transit-gateway still accounted for **1,872 of 2,504 PacketDropBurst-affected jobs—74.8%**. That’s a clear concentration, though lower than the external-only share of 87.2%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "network_inventory",
      "severity": "info",
      "title": "PacketDropBurst remained concentrated in transit-gateway",
      "description": "Transit-gateway represented 1,872 of 2,504 affected jobs after internal services were included, or approximately 74.8%.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied network inventory aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "PacketDropBurst total: 2,504 affected jobs; transit-gateway: 1,872."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains for this concentration calculation."
  }
}
```