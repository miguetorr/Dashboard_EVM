# Guía de configuración y pruebas — EVM Tracker

Guía paso a paso para configurar, ejecutar y probar el proyecto completo.

> **¿Por qué necesito Python Y Node.js?**
> El backend es **Python (FastAPI)** y el frontend es **React + TypeScript (Vite)**.
> Son dos aplicaciones separadas que se comunican vía API REST.

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
git clone <https://github.com/miguetorr/Dashboard_EVM.git>
cd Prueba-Tecnica
```

### 2.2 Instalar todo con el script de setup

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

Este script hace **automáticamente**:
1. Copia `.env.example` → `.env` (si no existe)
2. Crea el entorno virtual de Python (`.venv`)
3. Instala todas las dependencias de Python (`requirements.txt`)
4. Instala todas las dependencias de Node.js (`npm install`)
5. Verifica que Python, FastAPI y Node.js estén correctos

### 2.3 Ajustar variables de entorno (si es necesario)

El script crea el `.env` con valores por defecto. Si tu PostgreSQL tiene credenciales distintas, edita el archivo:

```env
# Conexión a PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/evm_tracker

# Orígenes permitidos para CORS
CORS_ORIGINS=http://localhost:5173
```

> **Importante:** El archivo `.env` debe estar en la **raíz del proyecto** (al mismo nivel que `backend/` y `frontend/`). El backend lo lee automáticamente gracias a `pydantic-settings`.

---

## 3. Configuración de la base de datos

Este es el único paso que **no** está automatizado (requiere PostgreSQL instalado y permisos del usuario).

### 3.1 Crear la base de datos

```bash
psql -U postgres -c "CREATE DATABASE evm_tracker;"
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

## 4. Levantar la aplicación

### 4.1 Con el script (recomendado)

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start.ps1
```

Levanta **backend y frontend juntos**. Muestra logs unificados con prefijo `[backend]` y `[frontend]`. Presiona `Ctrl+C` para detener ambos.

Una vez levantado:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/v1/projects
- **Documentación (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 4.2 Manual (si necesitas control individual)

<details>
<summary>Ver pasos manuales para levantar backend y frontend por separado</summary>

**Backend:**

```bash
cd backend
.venv\Scripts\Activate.ps1          # Windows
# source .venv/bin/activate          # Linux / macOS
uvicorn app.main:app --reload --port 8000
```

**Frontend** (en otra terminal):

```bash
cd frontend
npm run dev
```

</details>

---

## 5. Pruebas

### 5.1 Todo de una vez con el script (recomendado)

```powershell
powershell -ExecutionPolicy Bypass -File scripts\test.ps1
```

Ejecuta en secuencia:
1. **pytest** — 66 tests + reporte de cobertura (98%)
2. **flake8** — linter de Python
3. **tsc** — verificación de TypeScript
4. **eslint** — linter del frontend

### 5.2 Tests individuales (si necesitas depurar algo específico)

Los tests usan **SQLite en memoria** — no necesitan PostgreSQL ni configuración adicional.

<details>
<summary>Ver comandos individuales de tests</summary>

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

</details>

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

### 5.3 Linters individuales

<details>
<summary>Ver comandos individuales de linters</summary>

**Backend:**

```bash
cd backend
python -m flake8 app/
black --check app/
isort --check-only app/
```

**Frontend:**

```bash
cd frontend
npx tsc --noEmit
npx eslint src/            # o: npm run lint
npx prettier --check src/  # o: npm run format:check
```

</details>

### 5.4 Build de producción del frontend

```bash
cd frontend
npm run build
```

Genera los archivos optimizados en `frontend/dist/`.

---

## 6. Endpoints de la API para pruebas manuales

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

## 7. Validaciones que puedes probar

La API valida automáticamente y devuelve `422 Unprocessable Entity` si:

| Regla | Ejemplo que falla |
|-------|------------------|
| `bac` debe ser > 0 | `"bac": 0` o `"bac": -100` |
| `actual_cost` debe ser >= 0 | `"actual_cost": -1` |
| `planned_percentage` debe estar entre 0 y 100 | `"planned_percentage": 150` |
| `actual_percentage` debe estar entre 0 y 100 | `"actual_percentage": -5` |
| `name` es obligatorio y no puede estar vacío | `"name": ""` |

---

## 8. Edge cases del motor EVM

Escenarios especiales que la API maneja correctamente:

| Escenario | Comportamiento |
|-----------|---------------|
| `actual_cost = 0` | CPI = `null`, razón: "No se puede calcular: costo real es cero" |
| `planned_percentage = 0` | SPI = `null`, razón: "No se puede calcular: valor planificado es cero" |
| Todo en cero | PV, EV, AC = 0; CPI y SPI = `null` con razones descriptivas |
| Proyecto sin actividades | Todos los indicadores EVM en `null`, razón: "Datos insuficientes" |

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
