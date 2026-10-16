Yes. **checkout-api accounted for 421 of 486 minutes—about 87%** of the database connection-pool exhaustion downtime.

The remainder was:

- account-service: 43 minutes
- pricing-api: 22 minutes

So it was heavily concentrated in checkout-api.