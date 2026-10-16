Yes. Including primary and secondary lines, gpu-cluster-a accounted for 958 of 1,209 NodeUnavailable failures—about 79.2%, so a clear majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Most NodeUnavailable failures hit gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 958 of 1,209 NodeUnavailable-affected jobs, approximately 79.2%.",
      "location": "Shipment records for 2026-10-12; non-reserved inventory; primary and secondary production lines"
    }
  ]
}
```