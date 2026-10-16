Yes. On October 12, **FAB-A/CELL-ETCH-04** accounted for:

- **731 of 842 stockouts (86.8%)** on primary wafer-fab lines.
- **731 of 960 stockouts (76.1%)** across all wafer-fab and advanced-packaging lines.

So the stockouts were heavily concentrated in that single etch cell.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Servo-motor stockouts concentrated in one cell",
      "description": "FAB-A/CELL-ETCH-04 recorded 731 servo-motor stockouts, representing 86.8% of primary-line events and 76.1% of events across all production lines.",
      "location": "FAB-A/CELL-ETCH-04"
    }
  ]
}
```