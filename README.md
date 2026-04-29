# Dashboard EVM

Dashboard para el monitoreo de proyectos basada en la metodología **Earned Value Management (EVM)**. Permite registrar avance y costos en tiempo real, y calcular indicadores clave como PV, EV, AC, SPI y CPI para evaluar el desempeño del proyecto en cronograma y presupuesto.

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI (Python 3.11+) |
| Base de datos | PostgreSQL 15+ |
| Frontend | React 18 + TypeScript + Vite |
| Gráficas | Recharts |
| Documentación API | OpenAPI 3.1 (Swagger UI integrado) |

---

## Estructura del proyecto

```
├── backend/
│   ├── app/
│   │   ├── main.py                # Fábrica de la aplicación FastAPI
│   │   ├── config.py              # Configuración via pydantic-settings
│   │   ├── database.py            # Motor y sesión de SQLAlchemy
│   │   ├── exceptions.py          # Excepciones de dominio
│   │   ├── routers/               # Capa HTTP — solo enrutamiento
│   │   │   ├── projects.py
│   │   │   └── activities.py
│   │   ├── schemas/               # Pydantic: contratos solicitud/respuesta
│   │   │   ├── project.py
│   │   │   ├── activity.py
│   │   │   └── evm.py
│   │   ├── models/                # Modelos ORM de SQLAlchemy
│   │   │   ├── project.py
│   │   │   └── activity.py
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
│   │   ├── integration/
│   │   │   ├── test_projects_api.py
│   │   │   └── test_activities_api.py
│   │   └── conftest.py
│   ├── requirements.txt
│   ├── .flake8
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── components/
│   │   │   ├── ProjectCard.tsx
│   │   │   ├── ActivityTable.tsx
│   │   │   ├── ActivityModal.tsx
│   │   │   ├── EVMIndicators.tsx
│   │   │   ├── EVMChart.tsx
│   │   │   ├── EVMGlossary.tsx
│   │   │   ├── ProjectSelector.tsx
│   │   │   ├── ConfirmDialog.tsx
│   │   │   └── StatusBadge.tsx
│   │   ├── pages/
│   │   │   ├── ProjectListPage.tsx
│   │   │   └── ProjectDashboardPage.tsx
│   │   ├── utils/
│   │   │   └── evmCalculator.ts
│   │   ├── types/
│   │   │   └── evm.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── .eslintrc.cjs
├── sql/
│   ├── ddl.sql                    # Definición de tablas + constraints
│   └── seed.sql                   # Datos de ejemplo
├── openapi.yaml                   # Contrato de la API
├── .env.example                   # Variables de entorno de referencia
└── README.md
```

---

## Requisitos previos

- **Python** 3.11 o superior
- **Node.js** 18 o superior + npm
- **PostgreSQL** 15 o superior

---

## Configuración inicial

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Dashboard_EVM
```

### 2. Configurar variables de entorno

Copiar el archivo de ejemplo y ajustar los valores:

```bash
cp .env.example .env
```

Editar `.env` con los datos de tu instancia de PostgreSQL:

```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/evm_tracker
CORS_ORIGINS=http://localhost:5173
```

### 3. Crear la base de datos y cargar datos

```bash
# Crear la base de datos
psql -U postgres -c "CREATE DATABASE evm_tracker;"

# Ejecutar el DDL (tablas + constraints)
psql -U postgres -d evm_tracker -f sql/ddl.sql

# Cargar datos de ejemplo (opcional)
psql -U postgres -d evm_tracker -f sql/seed.sql
```

### 4. Levantar el backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor
uvicorn app.main:app --reload --port 8000
```

El backend estará disponible en `http://localhost:8000`.

### 5. Levantar el frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar el servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`.

---

## Documentación de la API

Una vez levantado el backend, la documentación interactiva está disponible en:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

El contrato OpenAPI también está disponible como archivo estático en `openapi.yaml` en la raíz del proyecto.

### Endpoints disponibles

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

---

## Tests

### Correr todos los tests

```bash
cd backend
pytest
```

### Correr tests con reporte de cobertura

```bash
pytest --cov=app --cov-report=term-missing
```

### Correr solo tests unitarios

```bash
pytest tests/unit/
```

### Correr solo tests de integración

```bash
pytest tests/integration/
```

El objetivo de cobertura es **≥ 80%** en lógica de negocio.

---

## Linters

### Backend

```bash
cd backend
flake8 app/
black --check app/
```

### Frontend

```bash
cd frontend
npx eslint src/
npx prettier --check src/
```

---

## Indicadores EVM

La aplicación calcula automáticamente los siguientes indicadores de Valor Ganado:

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

Los indicadores consolidados del proyecto se calculan por **suma de componentes** (estándar PMI): se suman PV, EV y AC de todas las actividades y luego se calculan los índices sobre esas sumas.
