Yes. Northbridge Laboratory accounted for 781 of 914 ReservationTagMismatch errors—about 85.4%, clearly the majority.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_event_analysis",
      "severity": "major",
      "title": "ReservationTagMismatch concentrated at Northbridge",
      "description": "Northbridge Laboratory generated 781 of the 914 reported ReservationTagMismatch events, representing approximately 85.4% of the total.",
      "location": "Inventory events report for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Compared the facility count of 781 with the reported error-type total of 914."
      },
      "evidence": {
        "text": "ReservationTagMismatch: 914 total events; Northbridge Laboratory: 781 events."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified interpretive conclusions remain from this calculation."
  }
}
```