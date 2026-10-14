Yes. **Cell-orion accounted for 1,936 of 2,214 NodeUnavailable failures—87.4%**. The remainder occurred in cell-polaris (187; 8.4%) and cell-vega (91; 4.1%), so the problem was strongly concentrated in cell-orion.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "operations-analysis",
      "severity": "major",
      "title": "NodeUnavailable concentrated in cell-orion",
      "description": "Cell-orion produced 1936 of the 2214 NodeUnavailable failures, representing approximately 87.4 percent.",
      "location": "Production primary lines, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied job_failures.aggregate result."
      },
      "evidence": {
        "text": "NodeUnavailable: cell-orion 1936, cell-polaris 187, cell-vega 91; total 2214."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains from this concentration assessment."
  }
}
```