Yes. EZE-1 accounted for 3,136 of 3,703 reported InventoryPickMismatch delays—about **84.7%**. It clearly represented the majority. The customer-facing-only slice was nearly identical at **85.0%** (1,824 of 2,146).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "delay_analytics",
      "severity": "info",
      "title": "EZE-1 accounted for most delays",
      "description": "EZE-1 represented 84.7% of all reported InventoryPickMismatch delays.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the reported facility counts: 3,136 divided by 3,703."
      },
      "evidence": {
        "text": "InventoryPickMismatch: EZE-1 3,136; total 3,703."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified interpretive judgments remain in this calculation."
  }
}
```