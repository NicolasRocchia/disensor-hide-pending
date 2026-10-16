Yes. **inventory-sync accounted for 2,739 of 3,288 TimeoutError downtime minutes—83.3%**.

The remainder was spread across:

- cell-replenisher: 298 min (9.1%)
- asrs-controller: 143 min (4.3%)
- allocation-scheduler: 108 min (3.3%)

So the TimeoutError problem was heavily concentrated in inventory-sync.