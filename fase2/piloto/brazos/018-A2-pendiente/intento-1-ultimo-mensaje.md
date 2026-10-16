Not yet determinable. The complete inventory query—including reserved compute capacity—was accepted asynchronously, but no result was returned. The non-reserved data alone showed strong concentration at North Campus Lab: 118 of 163 rotor stockouts (72.4%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Complete inventory result remains pending",
      "description": "The facility concentration after including reserved compute capacity cannot be determined until the asynchronous query returns.",
      "final_state": "escalated_open",
      "verification": {
        "against": "none",
        "detail": "Request req_inv_7K4M2Q was accepted, but its completed result was not provided."
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
        "description": "Retrieve the completed result for request req_inv_7K4M2Q before deciding whether rotor stockouts remained concentrated in one facility."
      }
    ]
  }
}
```