Yes. **Cell-atlas-3 accounted for 1,566 of the 1,842 servo-motor stockout delays—85.0%**. The remainder occurred in cell-atlas-1 (173; 9.4%) and cell-boreal-2 (103; 5.6%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Stockouts concentrated in cell-atlas-3",
      "description": "Cell-atlas-3 accounted for 1,566 of 1,842 delayed jobs caused by ServoMotorStockout, representing 85.0% of the total.",
      "location": "cell-atlas-3"
    }
  ]
}
```