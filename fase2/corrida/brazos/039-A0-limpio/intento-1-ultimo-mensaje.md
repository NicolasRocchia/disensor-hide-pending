Yes. Including secondary production lines, **production-api accounted for 2,161 of 2,525 TimeoutErrors—about 86%**.

- production-api: 2,161 (86%)
- worker: 277 (11%)
- scheduler: 87 (3%)

So the problem was strongly concentrated in `production-api`.