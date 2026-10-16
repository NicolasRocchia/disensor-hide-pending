Yes. Northbridge Analytical Campus accounted for **1,047 of 1,472 minutes**—about **71.1%**—of all reported temperature-excursion downtime yesterday. The next-highest facility, Río Plata BioLab, recorded 151 minutes.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "inventory_events.aggregate_async",
      "severity": "info",
      "title": "Northbridge dominated temperature-excursion downtime",
      "description": "Northbridge Analytical Campus accounted for 1,047 of 1,472 reported minutes, or approximately 71.1%.",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Calculated from the facility-level aggregation for yesterday across primary production lines and advanced packaging facilities."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved questions or unverified analytical gaps remained after calculating the facility share."
  }
}
```