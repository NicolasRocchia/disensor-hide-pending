Yes. TimeoutError downtime was heavily concentrated in `inventory-sync`:

- Including automated warehouse inventory: **2,739 of 3,288 minutes (83.3%)**
- Non-reserved inventory alone: **2,421 of 2,764 minutes (87.6%)**

No other service contributed more than 9.1%, so `inventory-sync` was clearly the main source.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutError concentrated in inventory-sync",
      "description": "Inventory-sync accounted for 2,739 of 3,288 TimeoutError downtime minutes (83.3%) across non-reserved and automated warehouse inventory.",
      "location": "robotics-inventory/inventory-sync"
    }
  ]
}
```