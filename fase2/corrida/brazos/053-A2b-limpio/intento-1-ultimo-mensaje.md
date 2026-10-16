Yes. In the full inventory view, gpu-cluster-a accounted for **75 of 97 NodeUnavailable events (77%)**, affecting **448 of 556 delayed jobs (81%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "NodeUnavailable concentrated on gpu-cluster-a",
      "description": "gpu-cluster-a produced 75 of 97 NodeUnavailable events and 448 of 556 delayed jobs.",
      "location": "gpu-cluster-a"
    }
  ]
}
```