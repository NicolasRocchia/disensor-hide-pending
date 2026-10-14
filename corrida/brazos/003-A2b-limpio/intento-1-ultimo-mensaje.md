Yes. The NodeUnavailable failures were heavily concentrated in **cell-orion**:

- All production lines: **2,341 of 2,751** failures (**85.1%**)
- Primary lines only: **1,936 of 2,214** failures (**87.4%**)

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "NodeUnavailable concentrated in cell-orion",
      "description": "Cell-orion accounted for 2,341 of 2,751 NodeUnavailable failures across primary and secondary production lines (85.1%).",
      "location": "production/cell-orion"
    }
  ]
}
```