Yes. On primary production lines, **cell-rack-assembly-3 accounted for 611 of 742 downtime minutes (82%)** and 25 of 31 delayed shipments (81%) caused by servo-motor stockouts. The remaining downtime was split between rack-assembly-1 (84 minutes) and cooling-module-2 (47 minutes).

The broader query including maintenance-only equipment was still pending, so this conclusion applies to primary production lines.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Servo-motor stockouts concentrated in rack-assembly cell 3",
      "description": "Cell-rack-assembly-3 accounted for 611 of 742 downtime minutes and 25 of 31 delayed shipments attributed to servo-motor stockouts on primary production lines.",
      "location": "cluster-hardware-plant/cell-rack-assembly-3"
    }
  ]
}
```