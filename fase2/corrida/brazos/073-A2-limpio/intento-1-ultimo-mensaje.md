Yes. The TimeoutError problem was heavily concentrated in `fleet-inventory-api`:

- 4,404 of 5,061 downtime minutes — **87.0%**
- 2,259 of 2,567 failed jobs — **88.0%**

By comparison, `supplier-sync-worker` caused 480 minutes and `allocation-scheduler` 177 minutes. The external-services-only view shows the same pattern: `fleet-inventory-api` accounted for 88.3% of TimeoutError downtime.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_jobs.aggregate_failures",
      "severity": "major",
      "title": "TimeoutError concentrated in fleet-inventory-api",
      "description": "The fleet-inventory-api accounted for 4404 of 5061 TimeoutError downtime minutes and 2259 of 2567 associated failed jobs.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the complete failure aggregation covering external services and reserved compute capacity."
      },
      "evidence": {
        "text": "fleet-inventory-api: 2259 failed jobs, 4404 downtime minutes"
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified execution gaps remain in this analysis."
  }
}
```