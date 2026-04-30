# Plan de pruebas — EVM Tracker v1

Estrategia, estructura y casos de prueba organizados por capa.

---

## Estrategia general

| Aspecto | Decisión |
|---------|----------|
| Framework backend | pytest |
| Cobertura objetivo | ≥ 80% en lógica de negocio (`core/`, `services/`) |
| Framework frontend | (opcional en V1, evaluar Vitest) |
| Reporte de cobertura | `pytest --cov=app --cov-report=term-missing` |
| Base de datos de tests | PostgreSQL de test (fixture con transacción que hace rollback) |
| Cliente HTTP de tests | `httpx.AsyncClient` con `TestClient` de FastAPI |

## Estructura de archivos

```
backend/tests/
├── conftest.py                    # Fixtures compartidas: DB test, client, proyecto y actividad de ejemplo
├── unit/
│   └── test_evm_calculator.py     # Tests puros del motor EVM
└── integration/
    ├── test_projects_api.py       # Tests de endpoints de proyectos
    └── test_activities_api.py     # Tests de endpoints de actividades
```

---

## 1. Tests unitarios — Motor EVM (`test_evm_calculator.py`)

### 1.1 Cálculo por actividad (`calculate_activity_evm`)

| # | Caso | Entrada | Resultado esperado |
|---|------|---------|-------------------|
| U01 | Caso estándar | bac=10000, plan=60, real=40, ac=7000 | PV=6000, EV=4000, CV=-3000, SV=-2000, CPI=0.5714, SPI=0.6667, EAC=17500.18, VAC=-7500.18 |
| U02 | Actividad completa en presupuesto | bac=5000, plan=100, real=100, ac=5000 | PV=5000, EV=5000, CV=0, SV=0, CPI=1.0, SPI=1.0, EAC=5000, VAC=0 |
| U03 | Bajo presupuesto y adelantado | bac=8000, plan=50, real=70, ac=3000 | CPI>1, SPI>1, estado_cpi="bajo_presupuesto", estado_spi="adelantado" |
| U04 | CPI y SPI exactamente 1 | bac=10000, plan=50, real=50, ac=5000 | CPI=1.0, SPI=1.0, estado_cpi="en_presupuesto", estado_spi="en_cronograma" |

### 1.2 Edge cases — divisiones por cero

| # | Caso | Entrada | Resultado esperado |
|---|------|---------|-------------------|
| U05 | AC=0 (CPI no calculable) | bac=5000, plan=20, real=10, ac=0 | CPI=null, razon_cpi="costo_real_es_cero", EAC=null, VAC=null, estado_cpi="datos_insuficientes" |
| U06 | PV=0 (SPI no calculable) | bac=5000, plan=0, real=10, ac=3000 | SPI=null, razon_spi="valor_planificado_es_cero", estado_spi="datos_insuficientes" |
| U07 | AC=0 y PV=0 (ambos null) | bac=5000, plan=0, real=0, ac=0 | CPI=null, SPI=null, CV=0, SV=0, ambas razones presentes |
| U08 | EV=0 con AC>0 | bac=5000, plan=50, real=0, ac=3000 | CPI=0.0, SPI=0.0, estado_cpi="sobre_presupuesto", estado_spi="atrasado" |
| U09 | CPI=0 → EAC no calculable | bac=5000, plan=50, real=0, ac=3000 | CPI=0 → EAC=null (BAC/0), VAC=null |

### 1.3 Cálculo consolidado (`calculate_project_evm`)

| # | Caso | Entrada | Resultado esperado |
|---|------|---------|-------------------|
| U10 | Múltiples actividades | A(PV=6000,EV=4000,AC=7000) + B(PV=10000,EV=6000,AC=8000) | PV_total=16000, EV_total=10000, AC_total=15000, CPI=0.6667, SPI=0.625 |
| U11 | Sin actividades (lista vacía) | [] | bac_total=0, todos los valores 0 o null |
| U12 | Todas las actividades con AC=0 | A(ac=0) + B(ac=0) | AC_total=0, CPI=null, razon_cpi="costo_real_es_cero" |
| U13 | Una sola actividad | A(bac=10000,...) | Consolidado = mismo valor que el cálculo individual |

### 1.4 Interpretación de estados

| # | Caso | Entrada | Resultado esperado |
|---|------|---------|-------------------|
| U14 | CPI > 1 | CPI=1.25 | "bajo_presupuesto" |
| U15 | CPI = 1 | CPI=1.0 | "en_presupuesto" |
| U16 | CPI < 1 | CPI=0.8 | "sobre_presupuesto" |
| U17 | CPI null | CPI=None | "datos_insuficientes" |
| U18 | SPI > 1 | SPI=1.5 | "adelantado" |
| U19 | SPI = 1 | SPI=1.0 | "en_cronograma" |
| U20 | SPI < 1 | SPI=0.7 | "atrasado" |
| U21 | SPI null | SPI=None | "datos_insuficientes" |

### 1.5 Precisión numérica

| # | Caso | Verificación |
|---|------|-------------|
| U22 | Redondeo CPI | EV=4000, AC=7000 → CPI=0.5714 (4 decimales) |
| U23 | Redondeo monetario | BAC=10000, CPI=0.5714 → EAC=17501.75 (2 decimales) |

---

## 2. Tests de integración — API de Proyectos (`test_projects_api.py`)

### 2.1 CRUD exitoso

| # | Caso | Método/Ruta | Verificación |
|---|------|-------------|-------------|
| I01 | Crear proyecto con nombre y descripción | POST `/projects` | 201, id UUID, name, description, timestamps |
| I02 | Crear proyecto sin descripción | POST `/projects` | 201, description=null |
| I03 | Listar proyectos | GET `/projects` | 200, array con proyectos + evm_consolidado |
| I04 | Listar sin proyectos | GET `/projects` | 200, array vacío |
| I05 | Detalle con actividades | GET `/projects/{id}` | 200, actividades con evm, evm_consolidado |
| I06 | Detalle sin actividades | GET `/projects/{id}` | 200, actividades=[], evm_consolidado con valores 0/null |
| I07 | Editar proyecto (nombre) | PUT `/projects/{id}` | 200, nombre actualizado, updated_at cambiado |
| I08 | Editar proyecto (descripción) | PUT `/projects/{id}` | 200, descripción actualizada |
| I09 | Eliminar proyecto | DELETE `/projects/{id}` | 204, proyecto ya no existe |

### 2.2 Errores y validaciones

| # | Caso | Método | Verificación |
|---|------|--------|-------------|
| I10 | Crear sin nombre | POST | 422, mensaje de validación |
| I11 | Crear con nombre vacío | POST `{"name": ""}` | 422 |
| I12 | Obtener proyecto inexistente | GET `/{uuid_falso}` | 404, "Proyecto no encontrado" |
| I13 | Editar proyecto inexistente | PUT `/{uuid_falso}` | 404 |
| I14 | Eliminar proyecto inexistente | DELETE `/{uuid_falso}` | 404 |

### 2.3 Cascade delete

| # | Caso | Verificación |
|---|------|-------------|
| I15 | Eliminar proyecto con actividades | DELETE proyecto → GET actividades del proyecto → 404 o lista vacía |

---

## 3. Tests de integración — API de Actividades (`test_activities_api.py`)

### 3.1 CRUD exitoso

| # | Caso | Método/Ruta | Verificación |
|---|------|-------------|-------------|
| I16 | Crear actividad completa | POST `/projects/{id}/activities` | 201, todos los campos + bloque evm calculado |
| I17 | Crear actividad con AC=0 | POST con actual_cost=0 | 201, evm.cpi=null, razon_cpi="costo_real_es_cero" |
| I18 | Listar actividades | GET `/projects/{id}/activities` | 200, array con evm por actividad |
| I19 | Listar sin actividades | GET | 200, array vacío |
| I20 | Editar actividad | PUT | 200, campos actualizados, evm recalculado |
| I21 | Eliminar actividad | DELETE | 204 |

### 3.2 Validaciones

| # | Caso | Entrada inválida | Verificación |
|---|------|-----------------|-------------|
| I22 | BAC = 0 | `{"bac": 0}` | 422 |
| I23 | BAC negativo | `{"bac": -500}` | 422 |
| I24 | AC negativo | `{"actual_cost": -100}` | 422 |
| I25 | Porcentaje > 100 | `{"actual_percentage": 105}` | 422 |
| I26 | Porcentaje < 0 | `{"planned_percentage": -5}` | 422 |
| I27 | Nombre vacío | `{"name": ""}` | 422 |

### 3.3 Errores de recurso

| # | Caso | Verificación |
|---|------|-------------|
| I28 | Crear en proyecto inexistente | 404, "Proyecto no encontrado" |
| I29 | Editar actividad inexistente | 404, "Actividad no encontrada" |
| I30 | Eliminar actividad inexistente | 404 |

### 3.4 EVM en respuestas

| # | Caso | Verificación |
|---|------|-------------|
| I31 | EVM calculado en crear | Response incluye pv, ev, cv, sv, cpi, spi, eac, vac, estados, razones |
| I32 | EVM recalculado en editar | Editar actual_cost → cpi/eac cambian |
| I33 | Consolidado actualizado | Crear actividad → GET proyecto → evm_consolidado refleja nueva actividad |

---

## 4. Fixtures (`conftest.py`)

| Fixture | Descripción |
|---------|-------------|
| `db_session` | Sesión de DB con transacción que hace rollback al terminar cada test |
| `client` | `TestClient` de FastAPI conectado a la DB de test |
| `sample_project` | Proyecto creado con nombre y descripción |
| `sample_activity` | Actividad creada dentro del proyecto de ejemplo con datos estándar |
| `project_with_activities` | Proyecto con 3 actividades variadas (buen estado, mal estado, AC=0) |

---

## Criterios de aceptación

- [ ] Todos los tests pasan (`pytest` sin fallos)
- [ ] Cobertura ≥ 80% en `app/core/` y `app/services/`
- [ ] Cada endpoint tiene al menos: caso exitoso, 404, 422 (si aplica)
- [ ] Edge cases EVM cubiertos: AC=0, PV=0, ambos cero, CPI=0
- [ ] Cascade delete verificado con test explícito
- [ ] No hay tests que dependan del orden de ejecución
