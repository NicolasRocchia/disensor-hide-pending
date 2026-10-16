Yes. Within customer-facing production systems, checkout-api accounted for 421 of 486 downtime minutes from database connection-pool exhaustion—86.6%. Account-service had 43 minutes and pricing-api 22 minutes.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Connection-pool exhaustion concentrated in checkout-api",
      "description": "checkout-api represented 421 of 486 downtime minutes (86.6%) attributed to database connection-pool exhaustion.",
      "location": "production logs, 2026-10-12, customer-facing systems"
    }
  ]
}
```