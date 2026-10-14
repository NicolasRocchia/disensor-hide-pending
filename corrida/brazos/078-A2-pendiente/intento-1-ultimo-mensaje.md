Yes. In standard compute pools, **FAB-L3 accounted for 143 of 184 WaferAlignTimeout-affected jobs—about 78%**, so it clearly represented most wafer-related delays. The maintenance-only equipment query had not completed, so this conclusion is limited to standard compute pools.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "telemetry_analysis",
      "severity": "info",
      "title": "FAB-L3 dominated wafer-related delays",
      "description": "FAB-L3 accounted for 143 of 184 jobs affected by WaferAlignTimeout, approximately 78 percent.",
      "location": "Standard compute pools, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the reported telemetry.aggregate_failures result."
      },
      "evidence": {
        "text": "WaferAlignTimeout affected 184 jobs: FAB-L3 143, FAB-L1 25, and FAB-L2 16."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The expanded query including maintenance-only equipment was accepted asynchronously, but no completed result was available.",
        "gap_reason": "other"
      }
    ]
  }
}
```