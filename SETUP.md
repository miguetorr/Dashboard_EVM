# Guía de configuración y pruebas — EVM Tracker

Guía paso a paso para configurar, ejecutar y probar el proyecto completo.

> **¿Por qué necesito Python Y Node.js?**
> El backend es **Python (FastAPI)** y el frontend es **React + TypeScript (Vite)**.
> Son dos aplicaciones separadas que se comunican vía API REST.

---

## Inicio rápido (3 comandos)

Si ya tienes Python, Node.js y PostgreSQL instalados:

```powershell
# 1. Configura todo (entorno virtual + dependencias Python + dependencias npm)
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1

# 2. Crea la base de datos (solo la primera vez)
psql -U postgres -c "CREATE DATABASE evm_tracker;"
psql -U postgres -d evm_tracker -f backend\database\schema.sql
psql -U postgres -d evm_tracker -f backend\database\seed.sql   # datos de ejemplo (opcional)

# 3. Levanta backend + frontend juntos
powershell -ExecutionPolicy Bypass -File scripts\start.ps1
```

Listo. Backend en http://localhost:8000, frontend en http://localhost:5173.

### Correr tests y linters (un solo comando)

```powershell
powershell -ExecutionPolicy Bypass -File scripts\test.ps1
```

Ejecuta: pytest + cobertura + flake8 + tsc + eslint, todo de una vez.

---

## Guía detallada (paso a paso)

### 1. Requisitos previos

| Herramienta | Versión mínima | Para qué | Verificar con |
|-------------|---------------|----------|---------------|
| Python | 3.11 | Backend (FastAPI, SQLAlchemy) | `python --version` |
| Node.js | 18 | Frontend (React, Vite) | `node --version` |
| PostgreSQL | 14 | Base de datos | `psql --version` |

> **Windows:** Si usas PowerShell, asegúrate de poder ejecutar scripts:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
> ```

---

## 2. Configuración del entorno

### 2.1 Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Prueba-Tecnica
```

### 2.2 Variables de entorno

Copiar el archivo de ejemplo y ajustar los valores según tu entorno:

```bash
# Linux / macOS
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
```

Contenido del `.env` (editar con tus credenciales):

```env
# Conexión a PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/evm_tracker

# Orígenes permitidos para CORS
CORS_ORIGINS=http://localhost:5173
```

> **Importante:** El archivo `.env` debe estar en la **raíz del proyecto** (al mismo nivel que `backend/` y `frontend/`). El backend lo lee automáticamente gracias a `pydantic-settings`.

---

## 3. Configuración de la base de datos

### 3.1 Crear la base de datos

```bash
# Conectarse a PostgreSQL como superusuario
psql -U postgres

# Dentro de psql:
CREATE DATABASE evm_tracker;
\q
```

### 3.2 Ejecutar el DDL (estructura de tablas)

```bash
psql -U postgres -d evm_tracker -f backend/database/schema.sql
```

Esto crea:
- Tabla `projects` (id UUID, name, description, timestamps)
- Tabla `activities` (id UUID, FK a projects, BAC, porcentajes, costo real, timestamps)
- CHECK constraints para validar rangos
- ON DELETE CASCADE para eliminación en cadena

### 3.3 Cargar datos de ejemplo (opcional)

```bash
psql -U postgres -d evm_tracker -f backend/database/seed.sql
```

Carga 2 proyectos con 3+ actividades cada uno, con escenarios variados (buen rendimiento, sobre presupuesto, AC=0).

### 3.4 Verificar que todo se creó correctamente

```bash
psql -U postgres -d evm_tracker -c "\dt"
```

Deberías ver las tablas `projects` y `activities`.

---

## 4. Configuración del backend

### 4.1 Crear y activar el entorno virtual

```bash
cd backend

# Crear entorno virtual
python -m venv .venv

# Activar:
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Windows (CMD):
.venv\Scripts\activate.bat

# Linux / macOS:
source .venv/bin/activate
```

> Sabrás que está activo cuando veas `(.venv)` al inicio del prompt.

### 4.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

Dependencias principales:
- **fastapi** 0.115.0 — Framework web
- **uvicorn** 0.30.6 — Servidor ASGI
- **sqlalchemy** 2.0.35 — ORM
- **psycopg2-binary** 2.9.9 — Driver PostgreSQL
- **pydantic** 2.9.2 — Validación de datos
- **pytest** 8.3.3 — Framework de tests

### 4.3 Iniciar el servidor de desarrollo

```bash
uvicorn app.main:app --reload --port 8000
```

Salida esperada:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

### 4.4 Verificar que funciona

Abre en el navegador:
- **Swagger UI (docs interactivos):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health check rápido:** http://localhost:8000/api/v1/projects (debería devolver `[]` o los datos del seed)

---

## 5. Configuración del frontend

### 5.1 Instalar dependencias

```bash
cd frontend
npm install
```

### 5.2 Iniciar el servidor de desarrollo

```bash
npm run dev
```

Salida esperada:
```
VITE v8.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

### 5.3 Verificar que funciona

Abre http://localhost:5173 en el navegador. Deberías ver la lista de proyectos (o el estado vacío con botón "+ Nuevo" si no cargaste el seed).

> **Nota:** El frontend se conecta al backend en `http://localhost:8000/api/v1`. Asegúrate de que el backend esté corriendo antes de abrir el frontend.

---

## 6. Pruebas

### 6.1 Tests del backend

Los tests usan **SQLite en memoria** — no necesitan PostgreSQL ni configuración adicional.

```bash
cd backend

# Ejecutar todos los tests
pytest

# Con reporte de cobertura detallado
pytest --cov=app --cov-report=term-missing

# Solo tests unitarios (motor EVM)
pytest tests/unit/

# Solo tests de integración (API completa)
pytest tests/integration/

# Un test específico
pytest tests/unit/test_evm_calculator.py::test_calculate_activity_evm_standard

# Ver output detallado
pytest -v
```

**Resultado esperado:**
```
66 passed
Coverage: 98%
```

| Suite | Archivo | Qué prueba |
|-------|---------|-----------|
| Unit | `tests/unit/test_evm_calculator.py` | Motor EVM: cálculos, redondeo, edge cases, interpretación de estados |
| Integration | `tests/integration/test_projects_api.py` | CRUD de proyectos, respuestas EVM, cascade delete, validaciones, 404s |
| Integration | `tests/integration/test_activities_api.py` | CRUD de actividades, validaciones de rango, edge cases EVM en respuestas |

### 6.2 Linters del backend

```bash
cd backend

# Verificar estilo con flake8
python -m flake8 app/

# Verificar formato con black (solo chequeo, no modifica)
black --check app/

# Verificar orden de imports
isort --check-only app/
```

### 6.3 Linters del frontend

```bash
cd frontend

# Verificar TypeScript (compilación sin emitir)
npx tsc --noEmit

# Verificar ESLint
npx eslint src/
# o equivalente:
npm run lint

# Verificar formato con Prettier (solo chequeo)
npx prettier --check src/
# o equivalente:
npm run format:check
```

### 6.4 Build de producción del frontend

```bash
cd frontend
npm run build
```

Genera los archivos optimizados en `frontend/dist/`.

---

## 7. Endpoints de la API para pruebas manuales

Puedes probar los endpoints directamente desde Swagger UI (http://localhost:8000/docs) o con `curl`:

### Crear un proyecto

```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Proyecto de prueba", "description": "Descripción del proyecto"}'
```

### Listar proyectos (con EVM consolidado)

```bash
curl http://localhost:8000/api/v1/projects
```

### Ver detalle de un proyecto (con actividades + EVM)

```bash
curl http://localhost:8000/api/v1/projects/{id}
```

### Crear una actividad

```bash
curl -X POST http://localhost:8000/api/v1/projects/{id}/activities \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Diseño",
    "bac": 50000,
    "planned_percentage": 60,
    "actual_percentage": 50,
    "actual_cost": 30000
  }'
```

### Editar una actividad

```bash
curl -X PUT http://localhost:8000/api/v1/projects/{id}/activities/{act_id} \
  -H "Content-Type: application/json" \
  -d '{"actual_percentage": 75, "actual_cost": 40000}'
```

### Eliminar un proyecto (cascade: elimina sus actividades)

```bash
curl -X DELETE http://localhost:8000/api/v1/projects/{id}
```

> **Tip:** Reemplaza `{id}` y `{act_id}` con los UUIDs reales devueltos por la API.

---

## 8. Validaciones que puedes probar

La API valida automáticamente y devuelve `422 Unprocessable Entity` si:

| Regla | Ejemplo que falla |
|-------|------------------|
| `bac` debe ser > 0 | `"bac": 0` o `"bac": -100` |
| `actual_cost` debe ser >= 0 | `"actual_cost": -1` |
| `planned_percentage` debe estar entre 0 y 100 | `"planned_percentage": 150` |
| `actual_percentage` debe estar entre 0 y 100 | `"actual_percentage": -5` |
| `name` es obligatorio y no puede estar vacío | `"name": ""` |

---

## 9. Edge cases del motor EVM

Escenarios especiales que la API maneja correctamente:

| Escenario | Comportamiento |
|-----------|---------------|
| `actual_cost = 0` | CPI = `null`, razón: "No se puede calcular: costo real es cero" |
| `planned_percentage = 0` | SPI = `null`, razón: "No se puede calcular: valor planificado es cero" |
| Todo en cero | PV, EV, AC = 0; CPI y SPI = `null` con razones descriptivas |
| Proyecto sin actividades | Todos los indicadores EVM en `null`, razón: "Datos insuficientes" |

---

## 10. Scripts de automatización

En la carpeta `scripts/` hay 3 scripts PowerShell para no tener que hacer los pasos manualmente:

| Script | Qué hace | Comando |
|--------|---------|---------|
| `setup.ps1` | Crea `.env`, entorno virtual Python, instala dependencias Python y npm | `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1` |
| `start.ps1` | Levanta backend y frontend juntos (Ctrl+C para detener) | `powershell -ExecutionPolicy Bypass -File scripts\start.ps1` |
| `test.ps1` | Ejecuta pytest + cobertura + flake8 + tsc + eslint de una vez | `powershell -ExecutionPolicy Bypass -File scripts\test.ps1` |

### Flujo rápido completo

```powershell
# Primera vez: setup + base de datos + iniciar
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
psql -U postgres -c "CREATE DATABASE evm_tracker;"
psql -U postgres -d evm_tracker -f backend\database\schema.sql
psql -U postgres -d evm_tracker -f backend\database\seed.sql
powershell -ExecutionPolicy Bypass -File scripts\start.ps1

# Siguientes veces: solo iniciar
powershell -ExecutionPolicy Bypass -File scripts\start.ps1

# Correr tests
powershell -ExecutionPolicy Bypass -File scripts\test.ps1
```

### Comandos manuales (si prefieres)

```bash
# === BACKEND ===
cd backend
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# === FRONTEND ===
cd frontend
npm install
npm run dev

# === TESTS ===
cd backend && pytest --cov=app --cov-report=term-missing
cd backend && python -m flake8 app/
cd frontend && npx tsc --noEmit
cd frontend && npm run lint
```

---

## Troubleshooting

| Problema | Solución |
|----------|---------|
| `psycopg2` no compila | Usa `psycopg2-binary` (ya incluido en requirements.txt) |
| CORS bloqueado | Verifica que `CORS_ORIGINS` en `.env` incluya `http://localhost:5173` |
| Puerto 8000 ocupado | Cambia con `uvicorn app.main:app --reload --port 8001` |
| Puerto 5173 ocupado | Vite elige automáticamente otro puerto, revisa la consola |
| `.env` no se carga | Debe estar en la raíz del proyecto, no dentro de `backend/` |
| Tests fallan con error de BD | Los tests usan SQLite en memoria, no necesitan PostgreSQL |
| `npx tsc` da errores | Ejecuta `npm install` primero para instalar tipos |
