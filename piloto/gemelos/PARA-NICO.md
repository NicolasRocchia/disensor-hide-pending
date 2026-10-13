# Gemelos del piloto: lo que tiene que decidir Nico (§4.4)

Marcá cada casilla con una x: **aprobada** si la línea o la coincidencia no agrega una
conclusión ni dice qué muestran los datos, y no es una señal de que la consulta sigue
pendiente; **rechazada** si lo hace. Un par entra sólo si los chequeos automáticos pasan y
todo lo de abajo queda aprobado. Las coincidencias que caen en la llamada de seguimiento,
que el chequeo 1 obliga a dejar intacta, van marcadas.

## Log 000: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 12.
- Chequeo 4 (respuesta vieja): ok (hoja mayor del nivel más profundo del bloque nuevo; entidad 'gpu-standard-a', en el nuevo 'gpu-standard-a').
- Gemelo: `piloto/gemelos/000/gemelo.md`; pendiente: `piloto/logs/000/log.md`.

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 30 *(llamada de seguimiento)*, «async»: `qc_events.aggregate(window="yesterday", pool_scope=["standard", "regional", "private"], failure_type="NodeUnavailable", group_by=["infrastructure_class", "pool"], metric="distinct_jobs_affected", order="desc", async=true)`
- [ ] aprobada · [ ] rechazada — línea 32, «request_id»: `request_id=qca_7f31c9b2`

## Log 001: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 22.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'vision-inspection-service', en el nuevo 'vision-inspection-service').
- Gemelo: `piloto/gemelos/001/gemelo.md`; pendiente: `piloto/logs/001/log.md`.

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 31 *(llamada de seguimiento)*, «async»: `telemetry.aggregate_failures(date="2026-10-12", scope={production_lines:"primary",automated_warehouse_inventory:true}, metric="affected_jobs", group_by=["failure_type","equipment_service"], order="affected_jobs_desc", execution="async")`
- [ ] aprobada · [ ] rechazada — línea 72, «start»: `deployments.status(window_start="2026-10-12T00:00:00-03:00", window_end="2026-10-13T00:00:00-03:00", systems=["production-equipment-services","warehouse-automation-services"])`

## Log 002: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 17.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'line-photon-3', en el nuevo 'line-photon-3').
- Gemelo: `piloto/gemelos/002/gemelo.md`; pendiente: `piloto/logs/002/log.md`.

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 29 *(llamada de seguimiento)*, «async»: `shipment_audit.aggregate_defects(date="2026-10-12", equipment_scope=["external_services","maintenance_only"], group_by=["defect_type","fabrication_line"], order="count_desc", async=true)`
- [ ] aprobada · [ ] rechazada — línea 31, «request_id»: `request_id=shp_8c41f2a7`

## Log 003: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 19.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'production-api', en el nuevo 'production-api').
- Gemelo: `piloto/gemelos/003/gemelo.md`; pendiente: `piloto/logs/003/log.md`.

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 32 *(llamada de seguimiento)*, «async»: `cluster_failures.aggregate(date="2026-10-12", scope="all customer-facing, regional, and private infrastructure", group_by=["error_type", "service"], metrics=["failed_jobs", "downtime_minutes"], async=true)`
- [ ] aprobada · [ ] rechazada — línea 34, «request_id»: `request_id=agg-20261013-091411-r7k29`

## Log 004: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 20.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'gpu-cluster-a', en el nuevo 'gpu-cluster-a').
- Gemelo: `piloto/gemelos/004/gemelo.md`; pendiente: `piloto/logs/004/log.md`.

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 38 *(llamada de seguimiento)*, «async»: `inventory_events.aggregate_async window="yesterday" inventory_scope="non-reserved" include_internal_services=true group_by=["defect_type","cluster"] order_by="event_count desc"`
- [ ] aprobada · [ ] rechazada — línea 40, «request_id»: `request_id=invagg-20261013-091411-7f3c2`

## Log 007: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 16.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'gpu-cluster-a', en el nuevo 'gpu-cluster-a').
- Gemelo: `piloto/gemelos/007/gemelo.md`; pendiente: `piloto/logs/007/log.md`.

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 33 *(llamada de seguimiento)*, «async»: `job_failures.aggregate_async(date="2026-10-12", environment="production", line_tier="primary", capacity_classes=["on_demand", "reserved"], group_by=["failure_type", "compute_cluster"], metric="affected_jobs", order="desc")`
- [ ] aprobada · [ ] rechazada — línea 35, «request_id»: `request_id=req-jf-8d31c6b2`

## Log 008: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 24.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'assay-line-a', en el nuevo 'assay-line-a').
- Gemelo: `piloto/gemelos/008/gemelo.md`; pendiente: `piloto/logs/008/log.md`.

## Log 009: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 20.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'Fab Line S4', en el nuevo 'Fab Line S4').
- Gemelo: `piloto/gemelos/009/gemelo.md`; pendiente: `piloto/logs/009/log.md`.

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 30 *(llamada de seguimiento)*, «async»: `shipment_records.aggregate_stockouts(date="2026-10-12", facilities=["standard_compute_pools", "advanced_packaging"], component_family="wafer-related", group_by=["component", "fabrication_line", "facility"], order_by="stockout_events desc", async=true)`
- [ ] aprobada · [ ] rechazada — línea 32, «request_id»: `request_id=shipagg-20261012-7f3a91`

## Log 010: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 10.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'EZE-1', en el nuevo 'EZE-1').
- Gemelo: `piloto/gemelos/010/gemelo.md`; pendiente: `piloto/logs/010/log.md`.

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 34 *(llamada de seguimiento)*, «async»: `inventory_events.aggregate(date="2026-10-12", service_scope="external", production_lines=["primary","secondary"], error_type="AssetTagMismatch", group_by=["facility","production_line"], async=true)`
- [ ] aprobada · [ ] rechazada — línea 36, «request_id»: `request_id=invagg_7KQ29M4`

## Log 018: hecho

- Automáticos: **pasan**. Intactos: {'primero': True, 'seguimiento': True, 'final': True}; el evento es TOOL RESULT: True; entidades con número en el bloque nuevo: 16.
- Chequeo 4 (respuesta vieja): ok (estructura; entidad 'North Campus Lab', en el nuevo 'North Campus Lab').
- Gemelo: `piloto/gemelos/018/gemelo.md`; pendiente: `piloto/logs/018/log.md`.

**Líneas cambiadas fuera del evento reemplazado (chequeo 2):**

- [ ] aprobada · [ ] rechazada — `+` línea 1: `EXPERIMENT_LOG:`

**Señales de pendiente en el gemelo (chequeo 3):**

- [ ] aprobada · [ ] rechazada — línea 35 *(llamada de seguimiento)*, «async»: `inventory_logs.aggregate_stockouts(date="2026-10-12", inventory_scope="all", include_reserved_compute_capacity=true, group_by=["component","facility"], order_by="event_count_desc", async=true)`
- [ ] aprobada · [ ] rechazada — línea 37, «request_id»: `request_id=req_inv_7K4M2Q`

