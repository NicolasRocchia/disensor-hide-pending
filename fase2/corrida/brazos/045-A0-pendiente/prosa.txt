Yes. In the customer-facing systems, **dispatch-api accounted for 1,947 of 2,184 TimeoutErrors—about 89%**.

- dispatch-api: 1,947 (89.1%)
- customer-tracking: 181 (8.3%)
- label-scheduler: 56 (2.6%)

So the problem was strongly concentrated in `dispatch-api`. The broader regional/private-infrastructure query had not yet returned.