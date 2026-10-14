Yes. Ashburn Assembly accounted for **2,311 of 3,000 affected jobs**, or **77.0%**, including Internal Services. Among the three facilities alone, it represented **81.2%** (2,311 of 2,846). So Ashburn clearly accounted for most of the ComponentQualificationFailure impact.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "manufacturing_delays.aggregate_async",
      "severity": "info",
      "title": "Ashburn accounted for most affected jobs",
      "description": "Ashburn Assembly represented 77.0% of all jobs affected by ComponentQualificationFailure, including Internal Services.",
      "location": "Manufacturing-delay records for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Compared Ashburn's 2,311 affected jobs with the reported total of 3,000."
      },
      "evidence": {
        "text": "ComponentQualificationFailure: Ashburn Assembly 2,311; total including Internal Services 3,000."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified interpretive judgments remained after comparing the reported counts."
  }
}
```