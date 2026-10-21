Yes. At **ashburn-dc3, 1,896 of 2,418 affected jobs (78.4%)** experienced `ManifestSyncTimeout`. Mesa accounted for 337 (13.9%) and Hillsboro for 185 (7.7%).

That conclusion applies to the three-facility results. The requested all-facility, internal-service analysis had not yet returned, so broader concentration remains unverified.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "shipment_analytics",
      "severity": "info",
      "title": "ManifestSyncTimeout concentrated at Ashburn",
      "description": "Ashburn-dc3 accounted for 1,896 of 2,418 affected jobs, or 78.4%, in the completed three-facility analysis.",
      "location": "Shipment failures for 2026-10-12",
      "final_state": "incorporated",
      "verification": {
        "against": "execution",
        "detail": "Calculated from the completed facility-facing aggregation."
      },
      "evidence": {
        "text": "ManifestSyncTimeout: ashburn-dc3 1,896; total 2,418 affected jobs."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous all-facility analysis including internal services was accepted but no completed result was provided, so the broader distribution could not be verified.",
        "gap_reason": "other"
      }
    ]
  }
}
```