Yes. Cordoba Central’s cell C-7 accounted for 873 of 1,124 affected jobs—77.7%. Rosario R-2 had 164 (14.6%), and Pilar P-4 had 87 (7.7%). So the reported servo-motor stockouts were strongly concentrated in C-7.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate",
      "severity": "major",
      "title": "Servo stockouts concentrated in cell C-7",
      "description": "Cordoba Central cell C-7 represented 77.7% of jobs affected by ServoMotorUnavailable across the three major facilities on 2026-10-12.",
      "location": "Cordoba Central / cell C-7",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied inventory aggregation result."
      },
      "evidence": {
        "text": "C-7 affected 873 of the 1,124 jobs impacted by ServoMotorUnavailable."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved residue remains within the reported three-facility aggregation."
  }
}
```