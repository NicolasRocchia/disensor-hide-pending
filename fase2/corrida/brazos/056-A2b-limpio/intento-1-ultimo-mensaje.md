Yes. Servo-motor stockouts were heavily concentrated in **cell-pack-04**:

- Customer-facing systems: **781 of 934 jobs (83.6%)**
- Including maintenance-only systems: **823 of 1,031 jobs (79.8%)**

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Servo-motor stockouts concentrated in cell-pack-04",
      "description": "Cell-pack-04 accounted for 781 of 934 affected customer-facing jobs (83.6%), or 823 of 1,031 jobs (79.8%) when maintenance-only systems were included.",
      "location": "robotics-west/cell-pack-04"
    }
  ]
}
```