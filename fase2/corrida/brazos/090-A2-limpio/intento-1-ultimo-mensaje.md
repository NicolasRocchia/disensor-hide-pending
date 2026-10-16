Yes. In customer-facing systems, **cell-orion-3 accounted for 392 of 486 servo-motor stockouts (80.7%)**, so they were strongly concentrated there.

Including advanced-packaging facilities, it remained the largest cell but represented **392 of 571 events (68.7%)**.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in cell-orion-3",
      "description": "Cell-orion-3 generated 392 of 486 customer-facing servo-motor stockout events, or 80.7%. Across the expanded scope including advanced packaging, it generated 392 of 571 events, or 68.7%.",
      "location": "Inventory-delay aggregation for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated directly from the supplied inventory-delay aggregation results."
      },
      "evidence": {
        "text": "servo-motor assembly: 486 customer-facing events, including 392 in cell-orion-3; 571 events in the expanded scope."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretation, execution gap, or decision requiring human attention remains."
  }
}
```