Yes. The TimeoutError problem was heavily concentrated in `fleet-inventory-api`:

- 4,404 of 5,061 downtime minutes — **87%**
- 2,259 of 2,567 failed jobs — **88%**

The remaining downtime came from `supplier-sync-worker` (480 minutes) and `allocation-scheduler` (177 minutes).

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "Timeout errors concentrated in fleet inventory API",
      "description": "fleet-inventory-api accounted for 4,404 of 5,061 TimeoutError downtime minutes (87%) and 2,259 of 2,567 associated failed jobs (88%).",
      "location": "robotics-inventory/fleet-inventory-api"
    }
  ]
}
```