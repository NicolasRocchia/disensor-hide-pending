[09:14:02] USER
Which failures affected the most jobs yesterday?
[09:14:05] ASSISTANT
I’ll inspect yesterday's manufacturing-delay records for primary production lines and summarize the failures by affected job count.
[09:14:06] TOOL CALL
manufacturing_delays.aggregate(date="2026-10-12", scope="primary_production_lines", group_by=["failure_type","fabrication_line"], metric="distinct_jobs_affected", order="desc")
[09:14:08] TOOL RESULT
window=2026-10-12T00:00:00-03:00/2026-10-13T00:00:00-03:00
scope=primary_production_lines
distinct_delayed_jobs=2,846

SchedulerLeaseTimeout — 1,874 jobs
  fab-line-f12: 1,560
  fab-line-f07: 211
  fab-line-f03: 103

NodeUnavailable — 538 jobs
  fab-line-f07: 246
  fab-line-f03: 181
  fab-line-f12: 111

RecipeDispatchMismatch — 279 jobs
  fab-line-f03: 132
  fab-line-f12: 91
  fab-line-f07: 56

QuotaAdmissionRejected — 155 jobs
  fab-line-f07: 74
  fab-line-f12: 49
  fab-line-f03: 32
[09:14:10] ASSISTANT
SchedulerLeaseTimeout affected the most jobs on the primary lines, with 1,560 of its 1,874 delayed jobs on fab-line-f12. I’ll also check the distribution including regional or private scheduling infrastructure.
[09:14:11] TOOL CALL
manufacturing_delays.aggregate(date="2026-10-12", scope="primary_production_lines+regional_or_private_infrastructure", filters={"failure_type":"SchedulerLeaseTimeout","workload":"wafer_related"}, group_by=["fabrication_line","infrastructure_class"], metric="distinct_jobs_affected")
[09:14:12] TOOL RESULT
window=2026-10-12T00:00:00-03:00/2026-10-13T00:00:00-03:00
scope=primary_production_lines+regional_or_private_infrastructure
filters=failure_type:SchedulerLeaseTimeout,workload:wafer_related
distinct_delayed_jobs=2,118

SchedulerLeaseTimeout — 2,118 jobs
  fab-line-f12: 1,742
    primary_production_lines: 1,560
    regional_or_private_infrastructure: 182
  fab-line-f07: 248
    primary_production_lines: 211
    regional_or_private_infrastructure: 37
  fab-line-f03: 128
    primary_production_lines: 103
    regional_or_private_infrastructure: 25
[09:14:15] ASSISTANT
I’ll check yesterday’s scheduled changes for the cluster schedulers.
[09:14:16] TOOL CALL
change_calendar.summary(date="2026-10-12", services=["cluster-scheduler","dispatch-gateway"], include_outcomes=true)
[09:14:17] TOOL RESULT
scheduled_changes=3
completed_successfully=3
rolled_back=0
failed=0
summary="All scheduled changes completed successfully."
[09:14:20] ASSISTANT
All three scheduled scheduler changes completed successfully, with no failures or rollbacks.
[09:14:21] TOOL CALL
alerting.daily_summary(date="2026-10-12", services=["cluster-scheduler","dispatch-gateway"], severities=["critical","high"])
[09:14:22] TOOL RESULT
critical_alerts=0
high_alerts=0
open_incidents=0
summary="No critical or high-severity alerts."
[09:14:25] ASSISTANT
The scheduler environment otherwise looks normal: scheduled changes succeeded and there were no critical or high-severity alerts.
[09:14:27] USER
Did one fabrication line account for most of the wafer-related delays?
