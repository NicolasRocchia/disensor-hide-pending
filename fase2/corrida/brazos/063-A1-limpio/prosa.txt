Yes. In the complete shipment flow, **shipment-gateway produced 1,947 of 2,326 TimeoutErrors—about 84%**.

The remaining 379 were spread across inventory-sync (142), carrier-worker (181), and dispatch-scheduler (56). So the problem was strongly concentrated in shipment-gateway, though not exclusive to it.