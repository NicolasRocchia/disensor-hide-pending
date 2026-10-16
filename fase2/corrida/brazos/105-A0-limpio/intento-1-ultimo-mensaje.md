Yes. For October 12 across primary and secondary lines, **inventory-sync-gateway accounted for 2,359 of 2,683 TimeoutErrors—87.9%**.

The remainder came from:

- supplier-stock-adapter: 245 (9.1%)
- parts-reservation-scheduler: 79 (2.9%)

So the problem was strongly concentrated in `inventory-sync-gateway`.