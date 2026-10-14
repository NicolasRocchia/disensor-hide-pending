Yes. In the external-services data, `fleet-inventory-api` accounted for **3,806 of 4,312 TimeoutError downtime minutes (88.3%)** and **1,947 of 2,184 failed jobs (89.1%)**. The problem was strongly concentrated there.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_jobs",
      "severity": "major",
      "title": "TimeoutError concentrated in fleet-inventory-api",
      "description": "The fleet-inventory-api produced approximately 88.3% of TimeoutError downtime and 89.1% of associated failed jobs in the external-services slice.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the inventory_jobs aggregate_failures result for yesterday."
      },
      "evidence": {
        "text": "fleet-inventory-api: 1,947 failed jobs, 3,806 downtime minutes"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretive, escalation, reviewer, or execution residue remained for this calculation."
  }
}
```