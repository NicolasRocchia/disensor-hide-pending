Yes—within standard compute pools, Fab Line S4 accounted for 231 of 286 wafer-carrier stockout events, or 80.8%. The other lines combined accounted for 55.

That establishes a clear majority by event count, but not necessarily by total delay duration. The broader query including advanced-packaging facilities was still pending.

```json
{
  "findings": [],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": true,
        "description": "The advanced-packaging aggregation remained pending, so the conclusion is limited to standard compute pools and stockout-event counts.",
        "gap_reason": "other"
      }
    ]
  }
}
```