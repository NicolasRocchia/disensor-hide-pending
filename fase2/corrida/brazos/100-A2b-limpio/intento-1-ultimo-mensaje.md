Yes. Servo-motor stockouts were heavily concentrated in **cell-pack-04**:

- Customer-facing scope: **914 of 1,126 jobs (81.2%)**
- Including automated warehouse inventory: **1,038 of 1,329 jobs (78.1%)**

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Stockouts concentrated in cell-pack-04",
      "description": "Cell-pack-04 accounted for 1,038 of 1,329 affected jobs (78.1%) in the expanded scope.",
      "location": "cell-pack-04"
    }
  ]
}
```