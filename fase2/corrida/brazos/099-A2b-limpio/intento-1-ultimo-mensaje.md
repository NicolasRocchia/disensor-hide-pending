Yes. The TimeoutError downtime was heavily concentrated in **lithography-dispatch**:

- **2,159 of 2,430 minutes** (88.8%) when reserved compute capacity is included
- **44 of 58 incidents** (75.9%)

The remaining downtime came from etch-control (215 minutes) and lot-scheduler (56 minutes).

{"findings":[{"id":"h1","origin":"assistant","severity":"info","title":"TimeoutError concentrated in lithography-dispatch","description":"Lithography-dispatch accounted for 2,159 of 2,430 TimeoutError downtime minutes (88.8%) and 44 of 58 incidents (75.9%) on 2026-10-12.","location":"Primary production lines / lithography-dispatch"}]}