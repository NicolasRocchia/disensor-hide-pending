Yes—within the **customer-facing production slice**, it was heavily concentrated in `shipment-gateway`:

- `shipment-gateway`: 1,947 of 2,184 TimeoutErrors (**89.1%**)
- `carrier-worker`: 181 (**8.3%**)
- `dispatch-scheduler`: 56 (**2.6%**)

The broader query including automated warehouse inventory had not returned, so I can’t confirm whether this concentration held across the complete shipment flow.