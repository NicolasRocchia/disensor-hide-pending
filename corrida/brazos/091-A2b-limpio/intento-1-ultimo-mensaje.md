Yes. Cell A3 accounted for 1,400 of 1,709 minutes—about **82%** of servo-motor stockout downtime. B1 contributed 186 minutes (11%) and C2 123 minutes (7%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Servo-motor stockouts concentrated in cell A3",
      "description": "Cell A3 represented approximately 82% of the 1,709 downtime minutes attributed to servo-motor stockouts.",
      "location": "Production cell A3"
    }
  ]
}
```