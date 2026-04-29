## Contexto

Proyecto greenfield — no existe código previo. Stack definido: FastAPI (Python), PostgreSQL, React. Es una herramienta interna para líderes de proyecto que necesitan medir salud de sus proyectos mediante Earned Value Management (EVM).

V1 sin autenticación — todos los usuarios ven todos los proyectos. La arquitectura debe permitir incorporar auth en V2 sin modificar contratos internos.

Los cálculos EVM son funciones puras y deterministas: datos de entrada → indicadores. No dependen de estado externo ni de IO.

## Objetivos / Fuera de alcance

**Objetivos:**

- API REST documentada con OpenAPI bajo prefijo `/api/v1/`
- Arquitectura en capas con contratos explícitos entre cada capa (Pydantic schemas, interfaces de repositorio, funciones puras EVM)
- Lógica de negocio aislada de transporte HTTP y de persistencia
- Cálculo EVM consolidado por suma de componentes (estándar PMI)
- Manejo explícito de edge cases (divisiones por cero) con null + razón en español
- Tests unitarios para EVM calculator, tests de integración por endpoint, cobertura ≥ 80% lógica de negocio
- Frontend reactivo con cálculo local, sin esperar ida y vuelta al servidor
- Código limpio: linter configurado, cero code smells, nombres descriptivos

**Fuera de alcance:**

- Autenticación y autorización (V2)
- Migraciones con Alembic (V2)
- Soft delete / historial de cambios (V2)
- WebSockets / notificaciones en tiempo real entre usuarios
- Internacionalización (solo español)
- Exportación de reportes (PDF, CSV)
- Gestión de usuarios y roles

## Decisiones

### 1. Arquitectura backend: Capas con contratos explícitos

**Decisión**: Router → Service → Repository + EVM Calculator como módulo puro.

**Alternativas consideradas**:
- **MVC clásico**: Mezcla lógica en controladores. Descartado — los requerimientos lo prohíben explícitamente.
- **Hexagonal completa**: Demasiada ceremonia para V1 con 2 entidades. Descartado por over-engineering.
- **Capas con interfaces**: Separación clara, testeable, flexible. **Elegida**.

**Estructura**:

```
backend/
├── app/
    ├── main.py                    # Fábrica de la aplicación FastAPI
    ├── config.py                  # Configuración via pydantic-settings
    ├── database.py                # Motor y sesión de SQLAlchemy
│   ├── routers/
    │   ├── projects.py            # Capa HTTP — solo enrutamiento
│   │   └── activities.py
│   ├── schemas/
    │   ├── project.py             # Pydantic: contratos de solicitud/respuesta
│   │   ├── activity.py
│   │   └── evm.py                 # EVMResult, EVMConsolidated
│   ├── models/
    │   ├── project.py             # Modelos ORM de SQLAlchemy
│   │   └── activity.py
│   ├── services/
│   │   ├── project_service.py     # Orquesta repository + EVM
│   │   └── activity_service.py
│   ├── repositories/
    │   ├── base.py                # Repositorio base abstracto
│   │   ├── project_repository.py
│   │   └── activity_repository.py
│   ├── core/
    │   ├── evm_calculator.py      # Funciones puras — sin estado, sin E/S
│   │   └── evm_constants.py       # Estados y razones en español
│   └── exceptions.py              # Excepciones de dominio
├── tests/
│   ├── unit/
│   │   └── test_evm_calculator.py # Tests puros del motor EVM
│   ├── integration/
│   │   ├── test_projects_api.py
│   │   └── test_activities_api.py
│   └── conftest.py                # Fixtures compartidas
├── requirements.txt
├── .flake8                        # Configuración del linter
└── pyproject.toml
```

### 2. EVM Calculator como módulo puro

**Decisión**: Funciones puras sin clases, sin estado, sin dependencias externas.

**Justificación**: Los cálculos EVM son transformaciones `data → data`. No necesitan OOP. Una función `calculate_activity_evm(bac, planned_pct, actual_pct, actual_cost) → EVMResult` es la unidad mínima testeable. El consolidado es `calculate_project_evm(activities: list) → EVMConsolidated`.

**Alternativa descartada**: Clase EVMCalculator con métodos — agrega estado sin beneficio, complica testing sin razón.

### 3. Base de datos: PostgreSQL con CHECK constraints

**Decisión**: Validación en dos capas — Pydantic (capa API, feedback inmediato) y CHECK constraints (capa DB, integridad garantizada).

**Constraints en DB**:
- `bac > 0`
- `actual_cost >= 0`
- `planned_percentage BETWEEN 0 AND 100`
- `actual_percentage BETWEEN 0 AND 100`

**UUIDs como PK**: `gen_random_uuid()` de PostgreSQL. Evita IDs secuenciales predecibles.

### 4. Indicadores no se almacenan en DB

**Decisión**: Todos los valores EVM se calculan en runtime, nunca se persisten.

**Justificación**: Los indicadores son derivados de los datos almacenados. Persistirlos crearía riesgo de inconsistencia (actualizar un campo y olvidar recalcular). La DB es fuente de verdad de hechos, no de derivaciones.

**Compromiso**: Si hubiera miles de actividades por proyecto, el cálculo en runtime podría ser lento. Para V1 con volumen bajo, es irrelevante.

### 5. Edge cases: null + razón

**Decisión**: Cuando una división por cero impide el cálculo (CPI cuando AC=0, SPI cuando PV=0), el campo retorna `null` y un campo `razon_*` explica por qué en español.

**Alternativas descartadas**:
- Retornar 0: Engañoso — 0 tiene significado matemático diferente a "no calculable"
- Retornar Infinity: JSON no soporta Infinity nativo
- Lanzar excepción: No es un error — es un estado válido del dominio

### 6. Frontend: React con cálculo local

**Decisión**: El frontend recalcula indicadores localmente mientras el usuario edita, sin esperar HTTP. Al guardar, el backend confirma.

**Librería de gráficas**: Recharts — ligera, declarativa, buena integración con React, sin dependencias pesadas.

**Alternativas para gráficas**:
- Chart.js + react-chartjs-2: Más pesada, API imperativa
- D3: Excesivo para gráficas de barras simples
- Recharts: Ligera, declarativa, API nativa de React. **Elegida**.

**Estructura frontend**:

```
frontend/
├── src/
│   ├── api/
    │   └── client.ts              # Instancia de Axios + tipos
│   ├── components/
│   │   ├── ProjectCard.tsx
│   │   ├── ActivityTable.tsx
│   │   ├── ActivityModal.tsx
│   │   ├── EVMIndicators.tsx
│   │   ├── EVMChart.tsx
│   │   ├── EVMGlossary.tsx
│   │   ├── ProjectSelector.tsx
│   │   ├── ConfirmDialog.tsx
│   │   └── StatusBadge.tsx
│   ├── pages/
│   │   ├── ProjectListPage.tsx
│   │   └── ProjectDashboardPage.tsx
│   ├── utils/
│   │   └── evmCalculator.ts       # Misma lógica EVM, en TypeScript
│   ├── types/
│   │   └── evm.ts                 # Tipos compartidos
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
└── .eslintrc.cjs
```

### 7. Preparación para Auth V2

**Decisión**: Los services reciben un parámetro `principal` que en V1 es `AnonymousPrincipal` (autoriza todo). En V2 se reemplaza por `AuthenticatedPrincipal` sin cambiar firmas de servicio.

### 8. Versionado de API

**Decisión**: Prefijo `/api/v1/` desde el inicio. Cuando exista V2, los endpoints V1 siguen funcionando.

### 9. Linter y formato

**Decisión**: Flake8 + Black (backend), ESLint + Prettier (frontend). Configuración incluida en el repositorio.

## Riesgos / Compromisos

- **[Duplicación de lógica EVM en frontend y backend]** → Mitigación: la lógica frontend es solo para preview reactivo. El backend es la fuente de verdad. Tests cubren ambas implementaciones para garantizar paridad.
- **[Sin auth en V1 — cualquiera puede eliminar datos]** → Mitigación: herramienta interna, riesgo aceptable. Auth preparada para V2.
- **[Hard delete sin recuperación]** → Mitigación: diálogo de confirmación obligatorio en frontend. Datos de ejemplo para restaurar demos.
- **[Recharts como dependencia de gráficas]** → Compromiso aceptado: ligera, mantenida, suficiente para gráficas de barras. Si se necesitan gráficas más complejas en futuro, se puede migrar.
- **[Sin migraciones en V1]** → Riesgo: cambios de schema requieren DDL manual. Aceptable porque V1 es deploy inicial sin datos en producción.
