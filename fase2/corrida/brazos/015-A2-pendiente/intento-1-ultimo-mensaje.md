Yes. Within non-reserved inventory, **production-api accounted for 1,947 of 2,184 TimeoutErrors—89.1%**. The remaining 10.9% occurred in inventory-worker (181) and allocation-scheduler (56), so the problem was strongly concentrated in production-api.

The pending combined analysis including automated warehouse inventory was not returned, so this conclusion applies only to the completed non-reserved-inventory dataset.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "incident_analytics",
      "severity": "info",
      "title": "TimeoutErrors concentrated in production-api",
      "description": "Production-api generated 1,947 of 2,184 TimeoutErrors in non-reserved inventory, representing 89.1 percent of the total.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the completed incident aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "production-api: 1,947 of 2,184 TimeoutError incidents"
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous aggregation that also included automated warehouse inventory had been accepted but had not returned results.",
        "gap_reason": "other"
      }
    ]
  }
}
```