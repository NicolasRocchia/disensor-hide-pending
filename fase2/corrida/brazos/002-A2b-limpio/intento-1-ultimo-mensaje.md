Yes. On October 12, gpu-cluster-a accounted for:

- **699 of 914** NodeUnavailable failures (**76.5%**) across all inventory.
- **611 of 742** (**82.3%**) in non-reserved inventory alone.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "NodeUnavailable concentrated on gpu-cluster-a",
      "description": "gpu-cluster-a produced 699 of 914 NodeUnavailable failures (76.5%), so it accounted for a clear majority.",
      "location": "Manufacturing inventory events for 2026-10-12"
    }
  ]
}
```