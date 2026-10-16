Yes. The TimeoutError problem was heavily concentrated in **dispatch-api**:

- **2,301 of 2,612 events (88.1%)** across all infrastructure
- **1,947 of 2,184 events (89.1%)** in customer-facing systems

The remaining events affected customer-tracking (228) and label-scheduler (83).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in dispatch-api",
      "description": "Dispatch-api accounted for 2,301 of 2,612 TimeoutError events (88.1%) across customer-facing, regional, and private infrastructure.",
      "location": "shipment records for 2026-10-12"
    }
  ]
}
```