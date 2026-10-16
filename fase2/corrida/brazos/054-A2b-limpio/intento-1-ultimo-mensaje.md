Yes. North Hub accounted for most packet-loss downtime:

- Full production scope: 780 of 914 minutes (85.3%)
- Customer-facing systems only: 684 of 788 minutes (86.8%)

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "North Hub dominated packet-loss downtime",
      "description": "North Hub accounted for 780 of 914 packet-loss downtime minutes (85.3%) across the full production scope.",
      "location": "North Hub"
    }
  ]
}
```