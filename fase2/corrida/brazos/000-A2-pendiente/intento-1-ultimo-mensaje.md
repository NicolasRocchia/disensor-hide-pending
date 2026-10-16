Yes. Northbridge Analytical Center accounted for 418 of 555 reported facility-equipment defects—about 75.3%. Meridian reported 87 (15.7%), and Lakeside reported 50 (9.0%).

The broader query including warehouse inventory had not returned, so these figures cover the completed facility-equipment dataset only.

```json
{
  "findings": [],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous warehouse-inventory query had not returned, so its records could not be included in the facility comparison.",
        "gap_reason": "other"
      }
    ]
  }
}
```