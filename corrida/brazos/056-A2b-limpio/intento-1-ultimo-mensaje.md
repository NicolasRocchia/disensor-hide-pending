Yes. Servo-motor stockouts were heavily concentrated in **cell-pack-04**:

- Customer-facing systems: **781 of 934 jobs (83.6%)**
- Including maintenance-only systems: **823 of 1,031 jobs (79.8%)**

The next-highest cell had only 107 affected jobs.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Stockouts concentrated in cell-pack-04",
      "description": "Cell-pack-04 accounted for 823 of 1,031 affected jobs (79.8%) across customer-facing and maintenance-only systems.",
      "location": "cell-pack-04"
    }
  ]
}
```