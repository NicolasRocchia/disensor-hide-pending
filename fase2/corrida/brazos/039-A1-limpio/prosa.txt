Yes. Including secondary production lines, **production-api generated 2,161 of 2,525 TimeoutErrors—about 86%**. Worker accounted for 277 (11%) and scheduler 87 (3%).

So the errors were strongly concentrated in production-api, though event counts alone don’t establish the root cause or whether its error rate was unusually high relative to traffic.