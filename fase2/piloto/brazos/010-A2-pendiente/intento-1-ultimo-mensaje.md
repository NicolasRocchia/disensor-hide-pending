It cannot yet be determined across both production-line types because the secondary-line aggregation was still pending. For primary lines alone, EZE-1 accounted for 1,947 of 2,184 AssetTagMismatch errors—89.1%—but that does not establish the combined result.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Combined facility distribution unavailable",
      "description": "The primary-line data shows EZE-1 accounted for 89.1% of AssetTagMismatch errors, but the requested primary-plus-secondary aggregation had not returned.",
      "final_state": "escalated_open",
      "verification": {
        "against": "none",
        "detail": "The combined aggregation request was accepted asynchronously, but no result was present in the supplied record."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "escalation_without_decision",
        "finding_ref": "h1",
        "requires_human_attention": true,
        "description": "Retrieve request invagg_7KQ29M4 and compare each facility's count with the combined AssetTagMismatch total."
      }
    ]
  }
}
```