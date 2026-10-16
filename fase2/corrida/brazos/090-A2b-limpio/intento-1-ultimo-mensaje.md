Yes. In customer-facing systems, **cell-orion-3 accounted for 392 of 486 servo-motor stockouts (80.7%)**, indicating strong concentration there. Including advanced-packaging facilities, it still represented the largest share: **392 of 571 events (68.7%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in cell-orion-3",
      "description": "Cell-orion-3 generated 392 of 486 customer-facing servo-motor stockouts (80.7%), or 392 of 571 events (68.7%) when advanced-packaging facilities are included.",
      "location": "final-assembly-north/cell-orion-3"
    }
  ]
}
```