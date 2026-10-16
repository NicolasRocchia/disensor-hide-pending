Yes. **eze-1 accounted for 2,641 of 3,146 minutes—about 84%—of the reported damaged accelerator tray downtime.** The other two facilities combined accounted for 505 minutes.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate",
      "severity": "info",
      "title": "eze-1 dominated damaged tray downtime",
      "description": "eze-1 accounted for approximately 84% of the reported damaged accelerator tray downtime.",
      "location": "eze-1",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory aggregation: 2641 / 3146 = 83.95%."
      },
      "evidence": {
        "text": "Damaged accelerator tray: 3,146 total minutes; eze-1: 2,641 minutes."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains within the scope of the supplied downtime aggregation."
  }
}
```