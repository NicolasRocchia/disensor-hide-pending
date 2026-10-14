Yes. Servo-motor stockouts were heavily concentrated in **cell-alpha**, which recorded **598 of 672 incidents (89.0%)**. Cell-delta had 51 (7.6%) and cell-foxtrot had 23 (3.4%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Stockouts concentrated in cell-alpha",
      "description": "Cell-alpha accounted for 598 of 672 servo-motor stockouts (89.0%); cell-delta had 51 and cell-foxtrot had 23.",
      "location": "customer-facing systems / cell-alpha"
    }
  ]
}
```