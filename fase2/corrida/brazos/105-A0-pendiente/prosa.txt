Yes. In the reported external-service, primary-line slice, **inventory-sync-gateway accounted for 1,947 of 2,184 TimeoutErrors—89.1%**.

- supplier-stock-adapter: 181 (8.3%)
- parts-reservation-scheduler: 56 (2.6%)

So the problem was strongly concentrated in `inventory-sync-gateway`. The secondary-line query had not yet returned, so this conclusion applies only to primary lines.