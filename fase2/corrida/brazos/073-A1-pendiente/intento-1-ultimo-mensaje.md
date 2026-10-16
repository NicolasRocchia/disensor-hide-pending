Yes—within the completed external-services analysis, the problem was heavily concentrated in `fleet-inventory-api`:

- 3,806 of 4,312 downtime minutes (88%)
- 1,947 of 2,184 failed jobs (89%)

The remaining downtime came from `supplier-sync-worker` (389 minutes) and `allocation-scheduler` (117 minutes).

The broader query including reserved compute capacity was still pending, so I can’t honestly confirm whether that concentration holds across the complete failure distribution.