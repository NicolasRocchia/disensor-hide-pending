Yes. EZE-1 accounted for 2,183 of 2,648 NodeUnavailable failures—82.4%—across standard and maintenance-only pools. In standard pools alone, it represented 2,071 of 2,486 failures, or 83.3%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "job_failure_analytics",
      "severity": "info",
      "title": "EZE-1 dominated NodeUnavailable failures",
      "description": "EZE-1 accounted for 2,183 of 2,648 affected jobs across standard and maintenance-only pools.",
      "location": "EZE-1 facility, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied job failure aggregation."
      },
      "evidence": {
        "text": "NodeUnavailable: EZE-1 2,183 jobs; all facilities 2,648 jobs."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified analytical gaps remained after comparing the facility totals."
  }
}
```