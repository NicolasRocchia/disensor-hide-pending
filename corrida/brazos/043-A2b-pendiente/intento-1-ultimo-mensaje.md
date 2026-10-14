FAB-3 was the largest contributor, but the answer depends on scope:

- For **wafer-stage vacuum instability**, yes—FAB-3 caused **1,196 of 1,486 minutes (80.5%)**.
- Across **all reported wafer-fabrication delays**, FAB-3 caused **1,307 of 2,651 minutes (49.3%)**—the largest share, but not an outright majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "FAB-3 dominated vacuum-instability downtime",
      "description": "FAB-3 accounted for 1,196 of 1,486 downtime minutes from wafer-stage vacuum instability, or 80.5%.",
      "location": "2026-10-12 wafer-fabrication delay records, FAB-3"
    },
    {
      "id": "h2",
      "origin": "assistant",
      "severity": "info",
      "title": "FAB-3 led total downtime without a majority",
      "description": "Across all reported wafer-fabrication issues, FAB-3 accounted for 1,307 of 2,651 downtime minutes, or 49.3%.",
      "location": "2026-10-12 wafer-fabrication delay records"
    }
  ]
}
```