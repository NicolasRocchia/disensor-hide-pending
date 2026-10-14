Yes. Including warehouse workflows, gpu-cluster-a accounted for 2,512 of 3,293 NodeUnavailable-affected jobs—about 76.3%. Across only the three facilities, it was 2,319 of 2,846 jobs—about 81.5%.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Most failures occurred on gpu-cluster-a",
      "description": "gpu-cluster-a represented 76.3% of all NodeUnavailable-affected jobs in the complete distribution.",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Verified against the supplied QC aggregation: 2,512 of 3,293 affected jobs."
      },
      "evidence": {
        "text": "NodeUnavailable: 3,293 jobs total; gpu-cluster-a: 2,512 jobs."
      }
    }
  ],
  "residue": {
    "declared_absence": true,
    "declaration": "No unresolved interpretation, execution gap, escalation, or reviewer-related residue remains."
  }
}
```