Yes. In the customer-facing systems, **production-api accounted for 1,492 of 1,684 TimeoutError downtime minutes—about 89%**.

The remainder was:

- worker: 143 minutes (8.5%)
- scheduler: 49 minutes (2.9%)

So the TimeoutError problem was strongly concentrated in `production-api`.