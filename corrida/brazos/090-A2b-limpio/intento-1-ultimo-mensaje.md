Yes. In the customer-facing systems, **cell-orion-3 accounted for 392 of 486 servo-motor stockouts (80.7%)**. The remaining events were in cell-orion-1 (61) and cell-lyra-2 (33).

Even including advanced-packaging facilities, cell-orion-3 still represented the majority: **392 of 571 events (68.7%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in cell-orion-3",
      "description": "Cell-orion-3 recorded 392 of 486 servo-motor stockouts in customer-facing systems (80.7%), or 392 of 571 events when advanced-packaging facilities are included (68.7%).",
      "location": "2026-10-12 production inventory events"
    }
  ]
}
```