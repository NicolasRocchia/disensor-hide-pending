Yes. After internal services were included, transit-gateway still accounted for 1,872 of 2,504 PacketDropBurst-affected jobs—about **74.8%**. Internal services added 358 affected jobs but did not change the concentration materially.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "network_inventory",
      "severity": "info",
      "title": "PacketDropBurst concentrated in transit-gateway",
      "description": "Transit-gateway represented 1,872 of 2,504 affected jobs (74.8%) after internal services were included."
    }
  ]
}
```