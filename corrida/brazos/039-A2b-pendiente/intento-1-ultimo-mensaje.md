Yes. **production-api accounted for 1,947 of 2,184 TimeoutErrors (89.1%)**. Worker had 181 (8.3%), and scheduler had 56 (2.6%), so the problem was strongly concentrated in production-api.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in production-api",
      "description": "Production-api generated 1,947 of 2,184 TimeoutError events (89.1%); worker generated 181 and scheduler generated 56.",
      "location": "Cloud standard compute pools, 2026-10-12"
    }
  ]
}
```