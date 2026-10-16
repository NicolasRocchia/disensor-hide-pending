Yes. The TimeoutErrors were heavily concentrated in `vision-inspection-api`:

- Including automated-warehouse inventory: **2,259 of 2,628** TimeoutErrors (**86.0%**).
- Non-reserved inventory alone: **1,947 of 2,184** (**89.1%**).

So `vision-inspection-api` was clearly the primary source.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_event_analysis",
      "severity": "major",
      "title": "TimeoutErrors concentrated in vision-inspection-api",
      "description": "The service generated 2259 of 2628 TimeoutErrors after automated-warehouse inventory was included.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the QC event aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "vision-inspection-api: 2259 of 2628 TimeoutError events, or approximately 86.0%."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains for the service-concentration question."
  }
}
```