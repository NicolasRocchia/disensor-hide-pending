Yes. **inventory-sync accounted for 2,421 of 2,764 TimeoutError downtime minutes—87.6%**.

The remainder was:

- cell-replenisher: 257 min (9.3%)
- allocation-scheduler: 86 min (3.1%)

So the TimeoutError problem was strongly concentrated in inventory-sync.