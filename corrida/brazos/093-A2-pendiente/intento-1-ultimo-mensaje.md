Yes. DC-S1 accounted for 151 of 184 servo-motor stockouts—about **82%**. The remaining events occurred in DC-S2 (21; 11%) and DC-S4 (12; 7%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "incident_records",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in DC-S1",
      "description": "DC-S1 recorded 151 of the 184 servo-motor stockout events, approximately 82 percent.",
      "location": "Standard compute pools, 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied incident-record aggregation."
      },
      "evidence": {
        "text": "Servo-motor assembly: 184 total events; DC-S1: 151, DC-S2: 21, DC-S4: 12."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved analytical residue remains from the supplied stockout records."
  }
}
```