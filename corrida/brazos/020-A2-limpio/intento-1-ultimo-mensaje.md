Yes. Assembly-cell-A3 accounted for 487 of 612 SM-42 stockout incidents on primary production lines—79.6%. The remaining incidents were in B1 (79) and P2 (46), so the stockouts were strongly concentrated in A3.

Including maintenance-only equipment, A3 still represented 74.8% of all 651 incidents.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "stockout-analysis",
      "severity": "info",
      "title": "SM-42 stockouts concentrated in A3",
      "description": "Assembly-cell-A3 recorded 487 of the 612 SM-42 stockout incidents on primary production lines.",
      "location": "assembly-cell-A3",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied quality-incidents aggregate for 2026-10-12."
      },
      "evidence": {
        "text": "servo_motor_SM-42: A3 487, B1 79, P2 46; primary-line total 612."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical questions or unverified execution gaps remain for this concentration calculation."
  }
}
```