Yes. In the customer-facing production slice, **shipment-gateway accounted for 1,947 of 2,184 TimeoutErrors—about 89%**.

The remainder came from carrier-worker (181, 8%) and dispatch-scheduler (56, 3%). The broader shipment-flow query hadn’t completed, so this conclusion applies specifically to the customer-facing systems.