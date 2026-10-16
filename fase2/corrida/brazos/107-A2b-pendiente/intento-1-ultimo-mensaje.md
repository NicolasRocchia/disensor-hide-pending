Yes. On the primary production lines, **fab-line-p1 accounted for 1,917 of 2,284 WaferCarrierRouteTimeout-affected jobs—about 84%**. That indicates one line dominated the wafer-related delays.

The broader aggregation including advanced-packaging facilities had not returned, so this conclusion is limited to the primary lines.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Wafer delays concentrated on fab-line-p1",
      "description": "Fab-line-p1 accounted for 1,917 of 2,284 jobs affected by WaferCarrierRouteTimeout, approximately 84%, within the primary production lines.",
      "location": "shipment_monitor aggregate for 2026-10-12; primary_production_lines/fab-line-p1"
    }
  ]
}
```