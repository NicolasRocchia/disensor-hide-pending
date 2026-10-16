Yes. In non-reserved inventory, **litho-dispatch accounted for 1,926 of 2,184 ReticleSyncTimeout events (88.2%)**. The remainder came from wafer-routing (174; 8.0%) and mask-catalog (84; 3.8%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "ReticleSyncTimeout concentrated in litho-dispatch",
      "description": "Litho-dispatch generated 1,926 of 2,184 ReticleSyncTimeout events (88.2%) in non-reserved inventory on 2026-10-12.",
      "location": "inventory_events.aggregate: 2026-10-12, non_reserved"
    }
  ]
}
```