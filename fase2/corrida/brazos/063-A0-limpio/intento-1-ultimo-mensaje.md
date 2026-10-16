Yes. **shipment-gateway accounted for 1,947 of 2,326 TimeoutErrors—about 84%**.

The remainder came from:

- carrier-worker: 181 (8%)
- inventory-sync: 142 (6%)
- dispatch-scheduler: 56 (2%)

So the problem was strongly concentrated in shipment-gateway, though not exclusive to it.