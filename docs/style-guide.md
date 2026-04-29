# Guía de estilos y convenciones — EVM Tracker v1

Convenciones de código, naming, linting y patrones del proyecto.

---

## General

| Regla | Detalle |
|-------|---------|
| Idioma del código | Inglés (nombres de variables, funciones, clases, archivos) |
| Idioma de la UI | Español (textos visibles, mensajes de error, estados EVM) |
| Idioma de documentación | Español |
| Idioma de commits | Español, formato: `tipo(alcance): descripción` |
| Branching | Gitflow strict |

---

## Backend (Python)

### Herramientas

| Herramienta | Propósito | Configuración |
|-------------|-----------|---------------|
| **Black** | Formatter | `pyproject.toml` — line-length: 88 |
| **Flake8** | Linter | `.flake8` — max-line-length: 88 (compatible con Black), ignore E203, W503 |
| **isort** | Ordenar imports | `pyproject.toml` — profile: "black" |

### Naming

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Archivos | snake_case | `project_service.py` |
| Funciones | snake_case | `calculate_activity_evm()` |
| Clases | PascalCase | `ProjectService`, `ActivityCreate` |
| Constantes | UPPER_SNAKE_CASE | `ESTADO_BAJO_PRESUPUESTO` |
| Variables | snake_case | `bac_total`, `planned_percentage` |
| Schemas Pydantic | PascalCase, sufijo según uso | `ProjectCreate`, `ProjectResponse`, `EVMResult` |
| Modelos SQLAlchemy | PascalCase singular | `Project`, `Activity` |
| Routers | snake_case, plural | `projects.py`, `activities.py` |

### Estructura de imports

```python
# 1. Stdlib
from typing import Optional
from uuid import UUID

# 2. Third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# 3. Local
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService
```

### Patrones de código

**Routers** — solo enrutamiento, sin lógica de negocio:

```python
@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    return service.create(data)
```

**Services** — orquestan repositorios y cálculos:

```python
class ProjectService:
    def __init__(self, db: Session):
        self.repo = ProjectRepository(db)

    def create(self, data: ProjectCreate) -> ProjectResponse:
        project = self.repo.create(data)
        return ProjectResponse.model_validate(project)
```

**EVM Calculator** — funciones puras, sin clases ni estado:

```python
def calculate_activity_evm(
    bac: float,
    planned_pct: float,
    actual_pct: float,
    actual_cost: float,
) -> EVMResult:
    ...
```

### Manejo de errores

- **404**: Lanzar `HTTPException(status_code=404, detail="Proyecto no encontrado")` desde el service
- **422**: Dejar que Pydantic lo maneje automáticamente con validators
- **No capturar excepciones genéricas** salvo en middleware global

---

## Frontend (TypeScript / React)

### Herramientas

| Herramienta | Propósito | Configuración |
|-------------|-----------|---------------|
| **ESLint** | Linter | `.eslintrc.cjs` — extends: recommended + react-hooks |
| **Prettier** | Formatter | `.prettierrc` — singleQuote: true, semi: true, tabWidth: 2 |
| **TypeScript** | Tipado estricto | `tsconfig.json` — strict: true |

### Naming

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Componentes | PascalCase | `ProjectCard.tsx`, `EVMChart.tsx` |
| Hooks | camelCase con prefijo `use` | `useProjects()`, `useEvm()` |
| Funciones utilitarias | camelCase | `calculateActivityEvm()` |
| Tipos/Interfaces | PascalCase | `ProjectSummary`, `EVMResult` |
| Constantes | UPPER_SNAKE_CASE | `EVM_STATUS_COLORS` |
| Props interfaces | PascalCase + sufijo `Props` | `ProjectCardProps`, `StatusBadgeProps` |
| Archivos de componentes | PascalCase, `.tsx` | `ActivityModal.tsx` |
| Archivos de utilidades | camelCase, `.ts` | `evmCalculator.ts` |

### Estructura de un componente

```tsx
// 1. Imports
import { useState } from 'react';
import { StatusBadge } from './StatusBadge';
import type { ProjectSummary } from '../types/evm';

// 2. Types (props)
interface ProjectCardProps {
  project: ProjectSummary;
  onEdit: (project: ProjectSummary) => void;
  onDelete: (project: ProjectSummary) => void;
  onClick: (projectId: string) => void;
}

// 3. Component (function declaration, NO default export)
export function ProjectCard({ project, onEdit, onDelete, onClick }: ProjectCardProps) {
  // hooks
  // handlers
  // return JSX
}
```

### Reglas de componentes

- **Named exports** siempre, nunca `export default`
- **Un componente por archivo** (excepto componentes internos pequeños)
- **Props desestructuradas** en el parámetro de la función
- **Typescript estricto**: no usar `any`, preferir tipos explícitos
- **Estado local** con `useState`; no se necesita estado global en V1

---

## Base de datos (SQL)

### Naming

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Tablas | snake_case, plural | `projects`, `activities` |
| Columnas | snake_case | `planned_percentage`, `actual_cost` |
| Primary keys | `id` | `id UUID DEFAULT gen_random_uuid()` |
| Foreign keys | `{tabla_singular}_id` | `project_id` |
| Constraints | `chk_{tabla}_{descripcion}` | `chk_activities_bac_positive` |
| Índices | `idx_{tabla}_{columna}` | `idx_activities_project_id` |

### Tipos de datos

| Campo | Tipo SQL | Justificación |
|-------|----------|---------------|
| IDs | `UUID` | Evita IDs secuenciales predecibles |
| Monetarios (bac, actual_cost) | `DECIMAL(15,2)` | Precisión decimal exacta, hasta 13 dígitos enteros |
| Porcentajes | `DECIMAL(5,2)` | 0.00 a 100.00 con 2 decimales |
| Timestamps | `TIMESTAMPTZ` | Siempre con zona horaria |
| Textos cortos (nombres) | `VARCHAR(255)` | Límite razonable |
| Textos largos (descripción) | `TEXT` | Sin límite artificial |

---

## Git

### Formato de commits

```
tipo(alcance): descripción breve en español

Cuerpo opcional con más contexto.
```

**Tipos permitidos:**

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Solo documentación |
| `style` | Formato, sin cambio de lógica |
| `refactor` | Reestructuración sin cambiar comportamiento |
| `test` | Agregar o modificar tests |
| `chore` | Tareas de mantenimiento (deps, config) |

**Ejemplos:**

```
feat(api): agregar endpoint de listar proyectos con EVM consolidado
fix(evm): corregir redondeo de CPI a 4 decimales
test(evm): agregar tests para edge case AC=0
docs(readme): agregar instrucciones de setup de PostgreSQL
chore(deps): actualizar fastapi a 0.111
```

### Ramas (Gitflow)

| Rama | Propósito |
|------|-----------|
| `main` | Producción estable |
| `develop` | Integración de features |
| `feature/{nombre}` | Desarrollo de funcionalidad |
| `hotfix/{nombre}` | Correcciones urgentes |

---

## Principios de diseño

1. **SOLID** — Responsabilidad única en cada capa (routers no hacen lógica, services no hacen HTTP)
2. **DRY** — La lógica EVM está en un solo lugar por lenguaje (un módulo Python, un módulo TypeScript)
3. **KISS** — No agregar abstracción donde no se necesita. V1 no necesita inyección de dependencias compleja.
4. **Fail fast** — Validar en Pydantic (capa más cercana al usuario), defender en DB (CHECK constraints)
5. **Contratos explícitos** — Pydantic schemas son el contrato entre capas. Si un campo cambia, el tipo lo detecta.
