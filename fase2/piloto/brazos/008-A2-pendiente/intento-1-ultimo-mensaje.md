Yes. Assay-line-a had 211 of 248 NodeUnavailable failures—about 85.1%—so the clear majority occurred there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "NodeUnavailable concentrated on assay-line-a",
      "description": "Assay-line-a accounted for 211 of 248 NodeUnavailable events, approximately 85.1%.",
      "location": "Production logs for 2026-10-12, non-reserved inventory, primary lines",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Verified against the aggregate_errors query result supplied in the conversation."
      },
      "evidence": {
        "text": "NodeUnavailable: 248 total; assay-line-a: 211."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified conclusions remain for this calculation."
  }
}
```