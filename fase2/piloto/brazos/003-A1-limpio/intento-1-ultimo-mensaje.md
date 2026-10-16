Yes—mostly in `production-api`, though not exclusively.

Across the broader fleet, it accounted for:

- 1,768 of 2,163 downtime minutes (82%)
- 2,311 of 2,798 failed jobs (83%)

The remaining downtime was spread across `worker` (207 minutes), `regional-edge` (118), and `scheduler` (70). So the issue was strongly concentrated in `production-api`, but it affected several services.