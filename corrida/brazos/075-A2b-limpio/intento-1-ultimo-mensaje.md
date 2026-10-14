Yes. In customer-facing systems, **CELL-F12 accounted for 78 of 96 servo-motor stockouts (81.25%)**, so they were strongly concentrated there. Including internal services, CELL-F12 still represented **94 of 118 events (79.7%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in CELL-F12",
      "description": "CELL-F12 recorded 78 of 96 customer-facing servo-motor stockout events (81.25%). With internal services included, it recorded 94 of 118 events (79.7%).",
      "location": "FAB-NORTE/CELL-F12"
    }
  ]
}
```