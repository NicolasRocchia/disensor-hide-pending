Yes. Within customer-facing systems on October 12, `production-api` accounted for 1,947 of 2,184 `TimeoutError` failures—about 89%.

The remaining 237 were in `async-worker` (181) and `job-scheduler` (56). The broader environment query had not yet returned, so this conclusion is limited to customer-facing systems.