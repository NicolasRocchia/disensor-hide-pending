Yes. Including secondary production lines, **641 of 759 servo-motor stockouts (84.5%) occurred in cell-alpha**. The remaining 118 incidents were distributed across four other cells, so the stockouts were strongly concentrated in cell-alpha.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Servo-motor stockouts concentrated in cell-alpha",
      "description": "Cell-alpha accounted for 641 of 759 servo-motor stockouts (84.5%) across customer-facing systems, including secondary production lines.",
      "location": "production/cell-alpha"
    }
  ]
}
```