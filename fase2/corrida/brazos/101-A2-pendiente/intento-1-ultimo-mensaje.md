Yes. **Metrology-dispatch accounted for 1,947 of 2,184 affected jobs—89.1%**. The remainder was split between lot-tracker (181; 8.3%) and recipe-scheduler (56; 2.6%), so the problem was strongly concentrated in one service.

This conclusion covers the three fabrication facilities; the expanded warehouse-inventory query had not completed.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutError concentrated in metrology-dispatch",
      "description": "Metrology-dispatch accounted for 1947 of the 2184 jobs affected by TimeoutError, or 89.1 percent.",
      "location": "Quality-control aggregation for 2026-10-12 across Fab-Aurora, Fab-Cascade, and Fab-Mesa",
      "final_state": "incorporated",
      "verification": {
        "against": "external_source",
        "detail": "Calculated from the supplied quality-control aggregation result."
      },
      "evidence": {
        "text": "TimeoutError: 2184 affected jobs; metrology-dispatch: 1947, lot-tracker: 181, recipe-scheduler: 56."
      }
    }
  ],
  "residue": {
    "items": [
      {
        "id": "r1",
        "class": "execution_gap",
        "requires_human_attention": false,
        "description": "The asynchronous expanded-scope query including automated warehouse inventory had not returned, so concentration is established only for the completed three-facility fabrication scope.",
        "gap_reason": "other"
      }
    ]
  }
}
```