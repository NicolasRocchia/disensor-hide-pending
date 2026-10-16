Yes. **dispatch-api accounted for 2,301 of 2,612 TimeoutErrors—about 88%**.

The remaining errors were in customer-tracking (228, 9%) and label-scheduler (83, 3%). So the problem was strongly concentrated in dispatch-api, though not exclusive to it. It appeared across all three regions and infrastructure classes.