Yes. **lot-release-api accounted for 1,947 of 2,184 TimeoutErrors—89.1%**. The remainder came from manifest-worker (181; 8.3%) and dispatch-scheduler (56; 2.6%), so the problem was strongly concentrated in one service.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in lot-release-api",
      "description": "The lot-release-api produced 1,947 of 2,184 TimeoutErrors (89.1%); manifest-worker produced 181 and dispatch-scheduler produced 56.",
      "location": "Production semiconductor-fab shipment records for 2026-10-12"
    }
  ]
}
```