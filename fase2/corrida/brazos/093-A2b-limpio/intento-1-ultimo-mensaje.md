Yes. Servo-motor stockouts were heavily concentrated in **DC-S1**:

- Standard and reserved pools: **180 of 222 events (81.1%)**
- Standard pools alone: **151 of 184 events (82.1%)**

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in DC-S1",
      "description": "DC-S1 recorded 180 of 222 servo-motor stockouts across standard and reserved compute pools, representing 81.1% of the total.",
      "location": "Production cell DC-S1"
    }
  ]
}
```