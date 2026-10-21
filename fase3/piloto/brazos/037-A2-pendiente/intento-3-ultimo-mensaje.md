Yes. Among the three major facilities, **ashburn-core accounted for 2,087 of 2,416 jobs—86.4%—affected by GPU ECC failures** on October 12, 2026.

The fleet-wide query was still pending, so this conclusion is limited to those three facilities.

```json
{
  "findings": [],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The all-facilities aggregation had been accepted but had not returned, so the fleet-wide concentration could not be confirmed.",
        "gap_reason": "other"
      }
    ]
  }
}
```