Yes. Including both primary and secondary lines, gpu-cluster-a accounted for **958 of 1,209 NodeUnavailable failures (79.2%)**. On primary lines alone, it accounted for **846 of 1,032 (82.0%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "NodeUnavailable concentrated on gpu-cluster-a",
      "description": "gpu-cluster-a accounted for 958 of 1,209 NodeUnavailable-affected jobs across primary and secondary production lines.",
      "location": "shipment records for 2026-10-12"
    }
  ]
}
```