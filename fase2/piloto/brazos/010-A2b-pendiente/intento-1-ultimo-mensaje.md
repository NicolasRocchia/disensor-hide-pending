Not yet determinable. EZE-1 accounted for most primary-line AssetTagMismatch errors (1,947 of 2,184; 89.1%), but the secondary-line query had not returned, so the combined share cannot be calculated.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Combined facility result unavailable",
      "description": "The primary-and-secondary aggregation was accepted asynchronously but no completed result was retrieved, so the question cannot be answered conclusively.",
      "location": "inventory_events.aggregate request invagg_7KQ29M4"
    }
  ]
}
```