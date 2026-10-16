Yes. Transit-gateway accounted for **1,872 of 2,504 affected jobs (74.8%)** after internal services were included. Its count did not change; internal services added 358 affected jobs, reducing transit-gateway’s share from 87.2% to 74.8%, but it remained strongly concentrated there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "network_inventory",
      "severity": "major",
      "title": "PacketDropBurst concentrated in transit-gateway",
      "description": "Transit-gateway represented 1872 of 2504 jobs affected by PacketDropBurst after internal services were included.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the network inventory aggregation for 2026-10-12 with external and internal service visibility."
      },
      "evidence": {
        "text": "PacketDropBurst affected 2504 distinct jobs, including 1872 in transit-gateway."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remained after checking the reported service-level job counts."
  }
}
```