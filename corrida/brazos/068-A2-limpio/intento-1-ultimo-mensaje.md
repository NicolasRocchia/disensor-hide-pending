Yes. Line-etch-3 produced 1,087 of 1,436 VisionAlignmentError events on the primary lines—about **75.7%**, clearly the majority. Even including advanced packaging, it accounted for **67.1%** of all 1,621 events.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "telemetry-analysis",
      "severity": "info",
      "title": "Most alignment errors occurred on line-etch-3",
      "description": "Line-etch-3 generated 1,087 of 1,436 primary-line VisionAlignmentError events.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied telemetry aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "line-etch-3: 1,087 events; primary production lines: 1,436 total events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified interpretive conclusions remain from this calculation."
  }
}
```