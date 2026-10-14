Yes. **lithography-dispatch accounted for 2,159 of 2,430 TimeoutError downtime minutes—about 89%**—and 44 of 58 incidents. The issue was strongly concentrated in that service.

```json
{
  "findings": [
    {
      "id": "h1",
      "origin": "assistant",
      "severity": "major",
      "title": "TimeoutError concentrated in lithography-dispatch",
      "description": "Lithography-dispatch caused 2,159 of 2,430 TimeoutError downtime minutes (88.8%) and 44 of 58 incidents on the primary production lines, including reserved compute capacity.",
      "location": "primary production lines / lithography-dispatch"
    }
  ]
}
```