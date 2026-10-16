Yes. `inventory-sync` accounted for most TimeoutError downtime:

- Including automated warehouse inventory: **2,739 of 3,288 minutes (83.3%)**
- Non-reserved inventory alone: **2,421 of 2,764 minutes (87.6%)**

So the problem was strongly concentrated in `inventory-sync`, though other services contributed the remaining 12–17%.