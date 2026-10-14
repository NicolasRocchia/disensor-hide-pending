Yes. Servo-motor stockouts were heavily concentrated in **DC-S1**:

- Standard pools: 151 of 184 events (**82.1%**)
- Standard + reserved pools: 180 of 222 events (**81.1%**)

The remaining events were split between DC-S2 and DC-S4.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in DC-S1",
      "description": "DC-S1 accounted for 151 of 184 servo-motor stockouts in standard pools and 180 of 222 when reserved capacity was included.",
      "location": "Production cell DC-S1"
    }
  ]
}
```