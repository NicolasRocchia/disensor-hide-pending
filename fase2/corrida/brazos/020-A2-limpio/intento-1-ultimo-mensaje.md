Yes. Assembly-cell-A3 accounted for 487 of 612 servo-motor stockouts on primary production lines—79.6%. Even including maintenance-only equipment, it represented 487 of 651 incidents, or 74.8%. The stockouts were therefore strongly concentrated in A3.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant-analysis",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in A3",
      "description": "Assembly-cell-A3 recorded 487 of 612 primary-line SM-42 stockout incidents (79.6%), and 487 of 651 incidents (74.8%) when maintenance-only equipment was included.",
      "location": "assembly-cell-A3",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the supplied quality-incidents aggregation results for 2026-10-12."
      },
      "evidence": {
        "text": "assembly-cell-A3: 487; primary-line total: 612; expanded total: 651"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved uncertainty remains within the supplied incident data and stated equipment scopes."
  }
}
```