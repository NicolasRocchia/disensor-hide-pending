The external-services data showed strong concentration in transit-gateway: 1,872 of 2,146 affected jobs (87.2%). However, the internal-services query was only accepted and no result was returned, so we cannot confirm whether that concentration remained after internal services were included.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Internal-service distribution remains unconfirmed",
      "description": "Transit-gateway represented 87.2% of PacketDropBurst-affected jobs in the available external-services result, but the expanded query produced no completed result.",
      "final_state": "escalated_open",
      "verification": {
        "against": "none",
        "detail": "The asynchronous internal-services request was accepted, but its result was never retrieved."
      },
      "evidence": {
        "text": "External result: transit-gateway affected 1,872 of 2,146 PacketDropBurst jobs."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "escalation_without_decision",
        "finding_ref": "h1",
        "requires_human_attention": true,
        "description": "Retrieve request ninv-20261013-091411-a83f before deciding whether PacketDropBurst remained concentrated in transit-gateway after internal services were included."
      }
    ]
  }
}
```