Yes. Including reserved compute capacity, gpu-cluster-a accounted for 699 of 914 NodeUnavailable failures—about 76.5%. In non-reserved inventory alone, it was 611 of 742—about 82.3%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "NodeUnavailable concentrated on gpu-cluster-a",
      "description": "gpu-cluster-a produced 699 of 914 NodeUnavailable failures (76.5%) across the complete inventory scope on 2026-10-12.",
      "location": "inventory events / gpu-cluster-a"
    }
  ]
}
```