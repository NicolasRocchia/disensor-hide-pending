Yes. Dock 7 accounted for 1,044 of 1,372 customer-facing LabelMismatch errors—76.1%, clearly the majority. Including maintenance-only equipment, it was 1,079 of 1,431—75.4%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "LabelMismatch concentrated at Dock 7",
      "description": "Dock 7 generated 76.1% of customer-facing LabelMismatch errors (1,044 of 1,372). The expanded scope produced the same conclusion at 75.4% (1,079 of 1,431).",
      "location": "Shipment records for 2026-10-12, Dock 7"
    }
  ]
}
```