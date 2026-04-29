## Por qué

Necesitamos construir una herramienta interna que permita a los líderes de proyecto registrar el avance de sus actividades y entender, en tiempo real, si su proyecto va bien o mal en términos de cronograma y presupuesto. La metodología de análisis es **Valor Ganado (Earned Value Management)**, un estándar del PMI que relaciona el avance real con el costo incurrido para generar señales de alerta tempranas.

Actualmente no existe ninguna herramienta — los líderes no tienen visibilidad cuantitativa del estado de sus proyectos.

## Qué cambia

- **API REST completa** (FastAPI) para gestionar proyectos y actividades con cálculo automático de 8 indicadores EVM (PV, EV, CV, SV, CPI, SPI, EAC, VAC)
- **Cálculo EVM por actividad y consolidado por proyecto** usando suma de componentes (estándar PMI), con manejo de edge cases (AC=0, PV=0) retornando `null` + razón descriptiva en español
- **Interpretación automática** del estado de CPI y SPI en español (bajo_presupuesto, sobre_presupuesto, adelantado, atrasado, datos_insuficientes)
- **Frontend React** con dashboard de proyecto, lista de proyectos con navegación rápida, tabla de actividades con expansión progresiva, gráfica comparativa PV/EV/AC, y glosario EVM para usuarios no técnicos
- **Cálculo reactivo en cliente** — los indicadores se recalculan localmente al editar sin esperar al servidor
- **Validaciones en DB y API**: BAC > 0, AC >= 0, porcentajes 0-100, con CHECK constraints en PostgreSQL y validación Pydantic
- **OpenAPI/Swagger** documentado en `/docs`
- **Script SQL** con DDL + datos de ejemplo (seed)
- **Sin autenticación en V1** — arquitectura preparada para auth en V2 sin romper contratos
- **Hard delete** para proyectos (cascade) y actividades con diálogo de confirmación en frontend
- **Cobertura de tests ≥ 80%** en lógica de negocio, con tests unitarios para cálculo EVM, tests de integración por endpoint, y cobertura explícita de edge cases

## Capacidades

### Nuevas capacidades

- `project-management`: CRUD de proyectos (crear, listar, ver detalle, editar, eliminar con cascade). Incluye resumen con conteo de actividades e indicadores consolidados en la lista.
- `activity-management`: CRUD de actividades dentro de un proyecto (crear, listar, editar, eliminar). Validaciones de dominio: BAC > 0, AC >= 0, porcentajes 0-100. Campos: name, bac, planned_percentage, actual_percentage, actual_cost.
- `evm-calculation`: Motor de cálculo de Valor Ganado. Calcula PV, EV, CV, SV, CPI, SPI, EAC, VAC por actividad y consolidado por proyecto (suma de componentes). Manejo de divisiones por cero con null + razón. Interpretación de estados en español.
- `project-dashboard`: Dashboard frontend con indicadores consolidados, tabla de actividades (expansión "ver más"), gráfica PV/EV/AC por actividad, selector rápido de proyecto, glosario EVM colapsable, y cálculo reactivo en cliente.
- `database-schema`: Esquema PostgreSQL con tablas projects y activities, CHECK constraints, cascade delete, y script seed con datos de ejemplo.

### Capacidades modificadas

_(ninguna — proyecto nuevo)_

## Impacto

- **Stack nuevo**: FastAPI + PostgreSQL + React (no hay código previo)
- **API pública**: 9 endpoints REST bajo `/api/v1/` con contrato OpenAPI
- **Base de datos**: 2 tablas con constraints de integridad
- **Dependencias backend**: FastAPI, SQLAlchemy, Pydantic, psycopg2, pytest, httpx
- **Dependencias frontend**: React, librería de gráficas (por definir en diseño), cliente HTTP
- **Entregables**: README.md con instrucciones de setup, script SQL (DDL + seed), configuración de linter
