Yes. Cambridge Receiving Lab accounted for 231 of 286 affected jobs—about 80.8%—so it represented a clear majority. This covers the three major facilities’ production-and-shipping records; the broader all-facility query had not returned results.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_analytics",
      "severity": "info",
      "title": "Cambridge dominated seal-integrity defects",
      "description": "Cambridge Receiving Lab accounted for 231 of the 286 shipment jobs affected by reported seal-integrity failures, or approximately 80.8%.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the returned facility-level shipment analytics."
      },
      "evidence": {
        "text": "Cambridge: 231 jobs; all three major facilities: 286 jobs."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": true,
        "description": "The asynchronous all-facility query, including maintenance-only equipment and inspection defects, was accepted but no completed result was provided.",
        "gap_reason": "other"
      }
    ]
  }
}
```