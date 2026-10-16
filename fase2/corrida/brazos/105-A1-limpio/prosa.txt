Yes. In the expanded primary-and-secondary-line data, **inventory-sync-gateway accounted for 2,359 of 2,683 TimeoutErrors—about 88%**.

The issue was strongly concentrated there, though not exclusive:

- supplier-stock-adapter: 245 (9%)
- parts-reservation-scheduler: 79 (3%)

This conclusion applies only to the queried external services and production lines. The data shows concentration, but not the underlying cause.