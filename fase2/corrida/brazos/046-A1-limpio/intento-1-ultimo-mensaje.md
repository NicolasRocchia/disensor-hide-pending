Yes—mostly in `production-api`.

- Customer-facing scope: 1,947 of 2,184 TimeoutErrors (89%)
- Broader scope including packaging facilities: 1,947 of 2,470 (79%)

So it was strongly concentrated there, though not exclusive: `packaging-mes` had 212 and `async-worker` had 181. These counts show concentration, but don’t establish the root cause.