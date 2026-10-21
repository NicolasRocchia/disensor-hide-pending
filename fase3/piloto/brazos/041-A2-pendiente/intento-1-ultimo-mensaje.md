Yes. For customer-facing jobs, **fab-line-4 accounted for 1,846 of 2,314 WaferAlignmentDrift impacts—about 79.8%**, clearly the majority. The broader query including internal services had not completed, so that wider scope remains unconfirmed.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Fab-line-4 caused most customer-facing wafer delays",
      "description": "Fab-line-4 represented 1,846 of 2,314 affected customer-facing jobs attributed to WaferAlignmentDrift, approximately 79.8 percent.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied quality-control aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "WaferAlignmentDrift: 2,314 affected jobs; fab-line-4: 1,846."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous aggregation covering both customer-facing and internal services was accepted but no completed result was provided, so the broader distribution could not be confirmed.",
        "gap_reason": "other"
      }
    ]
  }
}
```