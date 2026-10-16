Yes. Córdoba Assembly accounted for 471 of 612 SD-48 stockout events—77.0%. Rosario Robotics had 92 (15.0%), and Pilar Integration had 49 (8.0%). The stockouts were strongly concentrated at Córdoba.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_review",
      "severity": "info",
      "title": "SD-48 stockouts concentrated at Córdoba",
      "description": "Córdoba Assembly recorded 471 of 612 SD-48 stockout events, representing 77.0% of the total.",
      "location": "Robotics factory inventory logs for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the facility-level inventory aggregation supplied in the conversation."
      },
      "evidence": {
        "text": "SD-48 events: Córdoba Assembly 471, Rosario Robotics 92, Pilar Integration 49; total 612."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified analytical gaps remain for this facility concentration calculation."
  }
}
```