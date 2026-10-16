Yes. Ashburn accounted for 731 of 914 SFP-25G-SR stockouts—about 80%—so a clear majority occurred there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Ashburn had most stockouts",
      "description": "Ashburn recorded 731 of the 914 SFP-25G-SR stockout events, approximately 80%.",
      "location": "production inventory logs for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated directly from the supplied production log result: 731 divided by 914."
      },
      "evidence": {
        "text": "SFP-25G-SR transceiver: 914 total stockout events; ashburn-dc2: 731."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified interpretive judgments remain in this calculation."
  }
}
```