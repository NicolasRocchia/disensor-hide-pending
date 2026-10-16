Yes. **inventory-sync accounted for 2,421 of 2,764 downtime minutes (87.6%)** from `TimeoutError`. The remainder was split between cell-replenisher (257 minutes, 9.3%) and allocation-scheduler (86 minutes, 3.1%).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutError concentrated in inventory-sync",
      "description": "Inventory-sync caused 2,421 of 2,764 TimeoutError downtime minutes (87.6%), indicating that the problem was strongly concentrated in one service.",
      "location": "inventory-sync"
    }
  ]
}
```