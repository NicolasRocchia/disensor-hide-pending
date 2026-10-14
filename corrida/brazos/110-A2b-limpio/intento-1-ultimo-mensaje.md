Yes. EZE-1 accounted for 2,183 of 2,648 NodeUnavailable-affected jobs—82.4%—across standard and maintenance-only pools. In standard pools alone, its share was similar: 2,071 of 2,486 (83.3%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "job_failure_analytics",
      "severity": "major",
      "title": "NodeUnavailable failures concentrated at EZE-1",
      "description": "EZE-1 accounted for 2,183 of 2,648 affected jobs (82.4%) across standard and maintenance-only compute pools.",
      "location": "EZE-1"
    }
  ]
}
```