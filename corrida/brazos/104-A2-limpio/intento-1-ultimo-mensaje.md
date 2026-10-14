Yes. Motion-control-east accounted for 401 of 512 ServoDrive-X9 stockouts across all infrastructure—78.3%. Within standard compute pools, it accounted for 349 of 418—83.5%. The stockouts were therefore strongly concentrated there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "qc_inventory",
      "severity": "info",
      "title": "ServoDrive-X9 stockouts concentrated in motion-control-east",
      "description": "Motion-control-east produced 401 of 512 ServoDrive-X9 stockout events across all included infrastructure and 349 of 418 within standard compute pools.",
      "location": "qc_inventory aggregate for 2026-10-12",
      "final_state": "refuted_verifiable",
      "verification": {
        "against": "execution",
        "detail": "Verified against the returned inventory aggregation counts."
      },
      "evidence": {
        "text": "ServoDrive-X9: 512 total events, including 401 at motion-control-east."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified conclusions remain from this inventory comparison."
  }
}
```