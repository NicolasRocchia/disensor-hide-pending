Yes. Across primary and secondary production lines, **cell-orion accounted for 2,341 of 2,751 NodeUnavailable failures—85.1%**. On primary lines alone, it represented **1,936 of 2,214—87.4%**. The problem was therefore heavily concentrated in cell-orion.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "NodeUnavailable concentrated in cell-orion",
      "description": "Cell-orion accounted for 85.1% of NodeUnavailable failures across primary and secondary production lines.",
      "location": "production/cell-orion",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied job_failures.aggregate_async result for 2026-10-12."
      },
      "evidence": {
        "text": "NodeUnavailable: cell-orion 2,341 of 2,751 affected jobs."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive issues or execution gaps remain for this calculation."
  }
}
```