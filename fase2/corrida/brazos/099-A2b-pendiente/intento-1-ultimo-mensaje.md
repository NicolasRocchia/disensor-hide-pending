Yes. **lithography-dispatch** accounted for 1,947 of 2,184 TimeoutError downtime minutes—about **89%**—across 39 of 51 incidents. The remainder was in etch-control (181 minutes) and lot-scheduler (56 minutes).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutError concentrated in lithography-dispatch",
      "description": "Lithography-dispatch caused 1,947 of 2,184 TimeoutError downtime minutes (89%) and 39 of 51 incidents.",
      "location": "Primary production lines / lithography-dispatch"
    }
  ]
}
```