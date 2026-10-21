Yes. EZE-1 accounted for 349 of 438 stockout events—79.7%. COR-2 had 54 (12.3%) and ROS-1 had 35 (8.0%), so the stockouts were strongly concentrated at EZE-1.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory-telemetry",
      "severity": "info",
      "title": "Fan-module stockouts concentrated at EZE-1",
      "description": "EZE-1 generated 349 of the 438 recorded 48V fan-module stockout events.",
      "location": "2026-10-12 facility-level stockout telemetry",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied telemetry aggregation for non-reserved inventory."
      },
      "evidence": {
        "text": "48V fan module: 438 total events; EZE-1: 349, COR-2: 54, ROS-1: 35."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified execution gaps remain for this facility-concentration calculation."
  }
}
```