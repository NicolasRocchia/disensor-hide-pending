Yes. In the non-reserved inventory data, **vision-inspection-api accounted for 1,947 of 2,184 TimeoutErrors—89.1%**.

The remainder came from:

- qc-label-worker: 181 (8.3%)
- lot-release-scheduler: 56 (2.6%)

So it was strongly concentrated in one service. The automated-warehouse query was still pending, so this conclusion applies only to the completed non-reserved inventory results.