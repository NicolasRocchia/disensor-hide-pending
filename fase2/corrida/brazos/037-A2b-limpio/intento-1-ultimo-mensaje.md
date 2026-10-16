Yes. Servo-motor stockouts were heavily concentrated in **cell-atlas-3**:

- Across all infrastructure: **1,912 of 2,382 delayed jobs (80.3%)**
- Customer-facing systems only: **1,566 of 1,842 (85.0%)**

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Stockouts concentrated in cell-atlas-3",
      "description": "Cell-atlas-3 accounted for 1,912 of 2,382 servo-motor-stockout delays across all infrastructure (80.3%), including 1,566 of 1,842 customer-facing delays (85.0%).",
      "location": "cell-atlas-3"
    }
  ]
}
```