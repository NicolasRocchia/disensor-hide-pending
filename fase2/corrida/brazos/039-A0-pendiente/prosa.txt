Yes. **production-api accounted for 1,947 of 2,184 TimeoutErrors—about 89%**.

The remainder came from worker (181, 8%) and scheduler (56, 3%), so the problem was strongly concentrated in production-api.