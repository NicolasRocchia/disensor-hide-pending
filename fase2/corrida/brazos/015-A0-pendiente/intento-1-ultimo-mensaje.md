Yes. In non-reserved inventory, **production-api caused 1,947 of 2,184 TimeoutErrors—about 89%**. The remainder came from inventory-worker (181) and allocation-scheduler (56).

The broader warehouse-inclusive query had not yet returned, so this conclusion applies only to non-reserved inventory.