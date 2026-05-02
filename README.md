# Dashboard EVM

Dashboard para el monitoreo de proyectos basada en la metodología **Earned Value Management (EVM)**. Permite registrar avance y costos en tiempo real, y calcular indicadores clave como PV, EV, AC, SPI y CPI para evaluar el desempeño del proyecto en cronograma y presupuesto.

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11+ · FastAPI · SQLAlchemy · Pydantic |
| Base de datos | PostgreSQL 14+ |
| Frontend | React 19 · TypeScript · Vite |
| Gráficas | Recharts |
| Tests | pytest (66 tests, 98% cobertura) |
| Documentación API | OpenAPI 3.1 (Swagger UI en `/docs`) |

---

## Requisitos previos

| Herramienta | Versión mínima | Verificar con |
|-------------|---------------|---------------|
| Python | 3.11 | `python --version` |
| Node.js | 18 | `node --version` |
| PostgreSQL | 14 | `psql --version` |

---

## Correr el proyecto localmente

### 1. Clonar el repositorio

```bash
git clone https://github.com/miguetorr/Dashboard_EVM.git
cd Dashboard_EVM
```

### 2. Instalar dependencias

```powershell
# Asegúrate de estar en la carpeta raíz del proyecto (donde está este README)
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

> Este script crea el entorno virtual de Python, instala dependencias backend y frontend, y genera el archivo `.env` con credenciales por defecto (`postgres:postgres@localhost:5432/evm_tracker`).
> Si tu PostgreSQL tiene credenciales distintas, edita el `.env` generado antes de pasar al paso 3.

### 3. Inicializar la base de datos

```bash
psql -U postgres -c "CREATE DATABASE evm_tracker;"
psql -U postgres -d evm_tracker -f backend/database/schema.sql
psql -U postgres -d evm_tracker -f backend/database/seed.sql     # datos de ejemplo (opcional)
```

> `schema.sql` crea las tablas. `seed.sql` carga datos de ejemplo para probar la app sin tener que ingresar datos manualmente.

### 4. Levantar la aplicación

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start.ps1
```

Listo:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

### 5. Correr tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts\test.ps1
```

Ejecuta de una vez: pytest + cobertura + flake8 + tsc + eslint. **Resultado esperado:** 66 tests, 98% cobertura.

---

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/projects` | Listar proyectos con EVM consolidado |
| POST | `/api/v1/projects` | Crear proyecto |
| GET | `/api/v1/projects/{id}` | Detalle con actividades y EVM |
| PUT | `/api/v1/projects/{id}` | Editar proyecto |
| DELETE | `/api/v1/projects/{id}` | Eliminar proyecto (cascade) |
| GET | `/api/v1/projects/{id}/activities` | Listar actividades con EVM |
| POST | `/api/v1/projects/{id}/activities` | Crear actividad |
| PUT | `/api/v1/projects/{id}/activities/{act_id}` | Editar actividad |
| DELETE | `/api/v1/projects/{id}/activities/{act_id}` | Eliminar actividad |

Documentación interactiva completa en http://localhost:8000/docs una vez levantado el backend.

---

## Indicadores EVM

| Indicador | Nombre | Fórmula |
|-----------|--------|---------|
| PV | Valor Planificado | `(% planificado / 100) × BAC` |
| EV | Valor Ganado | `(% real / 100) × BAC` |
| AC | Costo Real | Dato registrado por el usuario |
| CV | Variación de Costo | `EV − AC` |
| SV | Variación de Cronograma | `EV − PV` |
| CPI | Índice de Rendimiento de Costo | `EV / AC` |
| SPI | Índice de Rendimiento de Cronograma | `EV / PV` |
| EAC | Estimación al Completar | `BAC / CPI` |
| VAC | Variación al Completar | `BAC − EAC` |

Los indicadores consolidados del proyecto se calculan por **suma de componentes** (estándar PMI).

---

## Estructura del proyecto

```
├── backend/
│   ├── app/
│   │   ├── main.py                # Fábrica de la aplicación FastAPI
│   │   ├── config.py              # Configuración via pydantic-settings
│   │   ├── database.py            # Motor y sesión de SQLAlchemy
│   │   ├── exceptions.py          # Excepciones de dominio
│   │   ├── routers/               # Capa HTTP
│   │   │   ├── projects.py
│   │   │   └── activities.py
│   │   ├── schemas/               # Pydantic: contratos de API
│   │   │   ├── project.py
│   │   │   ├── activity.py
│   │   │   └── evm.py
│   │   ├── models/                # Modelos ORM
│   │   │   └── models.py
│   │   ├── services/              # Lógica de negocio
│   │   │   ├── project_service.py
│   │   │   └── activity_service.py
│   │   ├── repositories/          # Acceso a datos
│   │   │   ├── base.py
│   │   │   ├── project_repository.py
│   │   │   └── activity_repository.py
│   │   └── core/                  # Motor EVM (funciones puras)
│   │       ├── evm_calculator.py
│   │       └── evm_constants.py
│   ├── tests/
│   │   ├── unit/
│   │   │   └── test_evm_calculator.py
│   │   └── integration/
│   │       ├── conftest.py
│   │       ├── test_projects_api.py
│   │       └── test_activities_api.py
│   ├── database/
│   │   ├── schema.sql             # DDL: tablas + constraints
│   │   └── seed.sql               # Datos de ejemplo
│   ├── requirements.txt
│   ├── .flake8
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts          # Cliente HTTP tipado (axios)
│   │   ├── components/
│   │   │   ├── ActivityModal.tsx
│   │   │   ├── ActivityTable.tsx
│   │   │   ├── ConfirmDialog.tsx
│   │   │   ├── EVMChart.tsx
│   │   │   ├── EVMGlossary.tsx
│   │   │   ├── EVMIndicators.tsx
│   │   │   ├── ProjectCard.tsx
│   │   │   ├── ProjectModal.tsx
│   │   │   ├── ProjectSelector.tsx
│   │   │   └── StatusBadge.tsx
│   │   ├── pages/
│   │   │   ├── ProjectListPage.tsx
│   │   │   └── ProjectDashboardPage.tsx
│   │   ├── utils/
│   │   │   └── evmCalculator.ts   # Motor EVM (cálculo reactivo)
│   │   ├── types/
│   │   │   └── evm.ts             # Tipos TypeScript
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── eslint.config.js
├── scripts/
│   ├── setup.ps1                  # Setup automático completo
│   ├── start.ps1                  # Levantar backend + frontend
│   └── test.ps1                   # Tests + linters de una vez
├── openapi.yaml                   # Contrato de la API
├── .env.example                   # Variables de entorno de referencia
└── README.md
```

---

## Guía detallada

Para instrucciones paso a paso manuales (sin scripts), troubleshooting y ejemplos de pruebas con `curl`, consulta [SETUP.md](SETUP.md).
