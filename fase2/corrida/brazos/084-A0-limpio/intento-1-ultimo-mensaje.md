Yes. Across primary and secondary lines, **pallet-vision-api** accounted for **1,602 of 1,972 downtime minutes (81%)** from `TimeoutError`, and **2,559 of 3,127 events (82%)**.

The remaining downtime was:

- weigh-station-gateway: 243 minutes (12%)
- label-verification-service: 127 minutes (6%)

So the problem was strongly concentrated in `pallet-vision-api`.