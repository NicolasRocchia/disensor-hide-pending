Yes. In the original non-reserved inventory scope, **vision-inspection-api produced 1,947 of 2,184 TimeoutErrors (89.1%)**. Even after including automated warehouse inventory, it remained dominant with **2,259 of 2,628 (86.0%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in vision-inspection-api",
      "description": "The service accounted for 89.1% of TimeoutErrors in non-reserved inventory and 86.0% when automated warehouse inventory was included.",
      "location": "quality-control events for 2026-10-12"
    }
  ]
}
```