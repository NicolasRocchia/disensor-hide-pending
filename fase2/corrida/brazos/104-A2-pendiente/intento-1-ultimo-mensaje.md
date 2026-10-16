Yes. **349 of 418 ServoDrive-X9 stockouts (83.5%)** occurred in `motion-control-east`. The remainder occurred in `assembly-orchestrator` (47; 11.2%) and `inspection-cell-standard` (22; 5.3%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_inventory",
      "severity": "info",
      "title": "ServoDrive-X9 stockouts were concentrated in motion-control-east",
      "description": "Motion-control-east accounted for 349 of the 418 ServoDrive-X9 stockout events, or 83.5%.",
      "final_state": "refuted_verifiable",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory aggregation for 2026-10-12."
      },
      "evidence": {
        "text": "ServoDrive-X9 — 418; motion-control-east: 349; assembly-orchestrator: 47; inspection-cell-standard: 22."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified interpretive judgments remain for this calculation."
  }
}
```