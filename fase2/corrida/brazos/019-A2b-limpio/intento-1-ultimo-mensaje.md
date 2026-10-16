Yes. Including maintenance-only equipment, **lot-release-api accounted for 2,031 of 2,296 TimeoutErrors (88.5%)**. The remainder came from manifest-worker (204; 8.9%) and dispatch-scheduler (61; 2.7%). The standard-pool-only data showed nearly the same concentration (89.1%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutErrors concentrated in lot-release-api",
      "description": "The lot-release-api produced 2,031 of 2,296 TimeoutErrors (88.5%), indicating that the problem was strongly concentrated in one service.",
      "location": "Production shipment records for 2026-10-12, standard and maintenance-only compute pools"
    }
  ]
}
```