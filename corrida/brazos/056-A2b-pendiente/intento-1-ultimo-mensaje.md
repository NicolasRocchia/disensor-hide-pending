Yes. **Cell-pack-04 accounted for 781 of 934 servo-motor stockout failures—about 84%**. The remainder affected cell-pack-02 (96 jobs) and cell-assembly-07 (57 jobs).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_ops",
      "severity": "major",
      "title": "Servo-motor stockouts concentrated in cell-pack-04",
      "description": "Cell-pack-04 accounted for 781 of 934 affected jobs (83.6%), indicating a strong concentration in one production cell.",
      "location": "robotics-west/cell-pack-04"
    }
  ]
}
```