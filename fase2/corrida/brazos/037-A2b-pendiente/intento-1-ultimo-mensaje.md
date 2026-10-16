Yes. The stockouts were heavily concentrated in **cell-atlas-3**, which accounted for **1,566 of 1,842 delayed jobs (85.0%)**. Cell-atlas-1 had 173, and cell-boreal-2 had 103.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Stockouts concentrated in cell-atlas-3",
      "description": "Cell-atlas-3 accounted for 1,566 of the 1,842 jobs delayed by servo-motor stockouts, or 85.0%.",
      "location": "2026-10-12 customer-facing systems, cell-atlas-3"
    }
  ]
}
```