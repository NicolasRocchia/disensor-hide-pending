Yes. In the October 12 combined inventory records, **production-api accounted for 2,359 of 2,793 TimeoutErrors—84.5%**. The remaining 15.5% was split among inventory-worker (277), allocation-scheduler (94), and warehouse-controller (63).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "incident_analytics",
      "severity": "major",
      "title": "TimeoutErrors concentrated in production-api",
      "description": "Production-api generated 84.5% of all TimeoutErrors in the combined inventory scope.",
      "location": "Incident records for 2026-10-12",
      "final_state": "owner_decision",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied incident aggregation results."
      },
      "risk_record": "Operational investigation should prioritize production-api.",
      "evidence": {
        "text": "Production-api accounted for 2,359 of 2,793 TimeoutError incidents."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical questions remain for the requested service-concentration assessment."
  }
}
```