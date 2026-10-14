Yes. In non-reserved inventory, Rosario accounted for **119 of 146 servo-motor SM-42 stockouts (81.5%)**. Córdoba had 18 and Santa Fe had 9. The automated-warehouse query had not completed, so this conclusion is limited to the available non-reserved inventory data.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "info",
      "title": "Servo-motor stockouts concentrated in Rosario",
      "description": "Rosario Assembly Plant recorded 119 of 146 SM-42 stockouts (81.5%) in non-reserved inventory on 2026-10-12.",
      "location": "inventory_incidents aggregate for 2026-10-12"
    }
  ]
}
```