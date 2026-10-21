Yes. EZE-1 accounted for 1,746 of 2,214 rack qualification hold minutes—about **78.9%**. COR-2 and ROS-1 combined accounted for the remaining 468 minutes (21.1%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "delay_analytics",
      "severity": "info",
      "title": "EZE-1 dominated rack qualification downtime",
      "description": "EZE-1 accounted for approximately 78.9% of rack qualification hold downtime.",
      "location": "2026-10-12 non-reserved inventory delay records",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated as 1,746 divided by 2,214 total downtime minutes."
      },
      "evidence": {
        "text": "EZE-1 recorded 1,746 of 2,214 rack qualification hold downtime minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty or execution gap remains for this calculation."
  }
}
```