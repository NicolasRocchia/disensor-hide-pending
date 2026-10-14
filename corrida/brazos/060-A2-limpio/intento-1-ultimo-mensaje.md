Yes. **FAB-LINE-07 accounted for 2,335 of 3,502 affected wafer jobs—66.7% of the total.** FAB-LINE-03 accounted for 674 (19.2%), and FAB-LINE-11 for 493 (14.1%). WarehouseLinkTimeout drove most of FAB-LINE-07’s impact.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "operations-analysis",
      "severity": "info",
      "title": "FAB-LINE-07 caused most wafer delays",
      "description": "FAB-LINE-07 accounted for 2335 of 3502 distinct affected wafer jobs, or 66.7 percent.",
      "location": "Inventory events for 2026-10-12, primary production lines and automated warehouse inventory",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the supplied inventory aggregation, deduplicated by job_id."
      },
      "evidence": {
        "text": "FAB-LINE-07 totals: 2148 + 104 + 45 + 38 = 2335 affected jobs."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains based on the supplied deduplicated inventory-event results."
  }
}
```