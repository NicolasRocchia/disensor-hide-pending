Yes—within non-reserved inventory, gpu-cluster-a accounted for:

- 61 of 76 events (80%)
- 366 of 438 delayed jobs (84%)
- 11,180 of 13,420 delay-minutes (83%)

So it was clearly the main source of NodeUnavailable failures. The broader query including reserved compute capacity was still pending.