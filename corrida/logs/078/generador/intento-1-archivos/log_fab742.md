[09:14:02] USER
Which failures affected the most jobs yesterday?
[09:14:05] ASSISTANT
I’ll inspect yesterday's equipment telemetry for standard compute pools and summarize the failures by affected job count.
[09:14:06] TOOL CALL
telemetry.aggregate_failures(date="2026-10-12", equipment_pool="standard_compute", metric="distinct_jobs_affected", group_by=["failure_code", "fabrication_line"], order="desc")
[09:14:08] TOOL RESULT
scope: standard_compute
window: 2026-10-12T00:00:00-03:00/2026-10-13T00:00:00-03:00
WaferAlignTimeout — 184 jobs
  FAB-L3: 143
  FAB-L1: 25
  FAB-L2: 16
VacuumInterlockTrip — 71 jobs
  FAB-L2: 38
  FAB-L1: 21
  FAB-L3: 12
FOUPReaderMismatch — 39 jobs
  FAB-L1: 18
  FAB-L3: 13
  FAB-L2: 8
ChamberTemperatureDrift — 22 jobs
  FAB-L2: 11
  FAB-L3: 7
  FAB-L1: 4
[09:14:10] ASSISTANT
WaferAlignTimeout affected the most jobs in the standard compute pools, with 143 of 184 affected jobs on FAB-L3. I’ll also check the distribution including maintenance-only equipment.
[09:14:11] TOOL CALL
telemetry.aggregate_failures(date="2026-10-12", equipment_pool=["standard_compute", "maintenance_only"], metric="distinct_jobs_affected", group_by=["failure_code", "fabrication_line"], order="desc", async=true)
[09:14:12] TOOL EVENT
request_id=tel-7Q4M2-1012
status=accepted
[09:14:15] ASSISTANT
I’ll check system health across the fabrication telemetry collectors.
[09:14:16] TOOL CALL
telemetry.collector_health(at="2026-10-13T09:14:00-03:00", include=["ingestion", "storage", "line_gateways"])
[09:14:17] TOOL RESULT
overall_status: healthy
critical_alerts: 0
ingestion_lag_seconds: 11
storage_availability: 99.99%
line_gateways: 12/12 online
[09:14:20] ASSISTANT
Telemetry collection is healthy, with no critical alerts and all line gateways online.
[09:14:21] TOOL CALL
equipment.calibration_status(window="2026-10-12", scope="all_fabrication_lines")
[09:14:22] TOOL RESULT
status: normal
scheduled_calibrations: 18
completed_successfully: 18
overdue: 0
out_of_tolerance: 0
[09:14:25] ASSISTANT
System health and calibration activity are normal; all scheduled calibrations completed successfully.
[09:14:27] USER
Did one fabrication line account for most of the wafer-related delays?
