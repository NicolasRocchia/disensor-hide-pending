Yes. The `TimeoutError` downtime was heavily concentrated in `fleet-inventory-api`:

- **4,404 of 5,061 minutes (87%)**
- **2,259 of 2,567 failed jobs (88%)**

The remaining downtime came from `supplier-sync-worker` (480 minutes) and `allocation-scheduler` (177 minutes). This shows concentration, but the aggregate data alone doesn’t prove the underlying root cause.