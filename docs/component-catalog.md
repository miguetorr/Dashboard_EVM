# Catálogo de componentes React — EVM Tracker v1

Jerarquía, responsabilidades y props de cada componente del frontend.

---

## Árbol de componentes

```
App
├── ProjectListPage
│   ├── ProjectCard (×N)
│   │   └── StatusBadge (×2: CPI, SPI)
│   ├── ProjectModal (crear/editar)
│   └── ConfirmDialog (eliminar proyecto)
│
└── ProjectDashboardPage
    ├── ProjectSelector (breadcrumb + dropdown)
    ├── EVMIndicators
    │   └── StatusBadge (×2: CPI, SPI)
    ├── EVMChart (Recharts)
    ├── ActivityTable
    │   ├── StatusBadge (×2 por fila)
    │   └── ConfirmDialog (eliminar actividad)
    ├── ActivityModal (crear/editar + vista previa EVM)
    │   └── StatusBadge (×2: preview CPI, SPI)
    └── EVMGlossary (panel colapsable)
```

---

## Páginas

### `ProjectListPage`

| Aspecto | Detalle |
|---------|---------|
| Ruta | `/projects` |
| Responsabilidad | Mostrar grid de tarjetas de proyectos. Botón "Nuevo proyecto". Orquestar crear/editar/eliminar proyecto. |
| Estado | Lista de proyectos (del API), modal abierto/cerrado, proyecto seleccionado para editar/eliminar |
| API calls | `GET /api/v1/projects`, `POST`, `PUT`, `DELETE` |

### `ProjectDashboardPage`

| Aspecto | Detalle |
|---------|---------|
| Ruta | `/projects/:id` |
| Responsabilidad | Mostrar dashboard completo de un proyecto: indicadores consolidados, tabla de actividades, gráfica, glosario. Orquestar CRUD de actividades. |
| Estado | Proyecto con actividades (del API), modal actividad abierto/cerrado, tabla expandida/colapsada |
| API calls | `GET /api/v1/projects/{id}`, CRUD actividades |

---

## Componentes compartidos

### `StatusBadge`

Muestra un badge de color según el estado de un indicador EVM.

| Prop | Tipo | Descripción |
|------|------|-------------|
| `status` | `'bajo_presupuesto' \| 'en_presupuesto' \| 'sobre_presupuesto' \| 'adelantado' \| 'en_cronograma' \| 'atrasado' \| 'datos_insuficientes'` | Estado EVM a representar |
| `label` | `string` | Texto del badge (ej. "CPI: 0.57") |

**Colores:**
- 🟢 Verde: `bajo_presupuesto`, `adelantado` (favorable)
- 🟡 Amarillo: `en_presupuesto`, `en_cronograma` (neutral)
- 🔴 Rojo: `sobre_presupuesto`, `atrasado` (desfavorable)
- ⚪ Gris: `datos_insuficientes` (no calculable)

### `ConfirmDialog`

Diálogo modal de confirmación para acciones destructivas.

| Prop | Tipo | Descripción |
|------|------|-------------|
| `open` | `boolean` | Controla visibilidad |
| `title` | `string` | Título del diálogo (ej. "Eliminar proyecto") |
| `message` | `string` | Mensaje descriptivo con nombre del recurso |
| `confirmLabel` | `string` | Texto del botón de confirmación (default: "Eliminar") |
| `onConfirm` | `() => void` | Callback al confirmar |
| `onCancel` | `() => void` | Callback al cancelar |

**Diseño:** Botón de confirmación en rojo, botón de cancelar en gris/neutro.

### `EVMGlossary`

Panel colapsable con definiciones de indicadores EVM en español.

| Prop | Tipo | Descripción |
|------|------|-------------|
| (sin props) | — | Componente autocontenido |

**Contenido:** Definición de BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC, VAC en lenguaje claro para no expertos. Se abre/cierra con botón "¿Qué significan estos indicadores?"

---

## Componentes de proyecto

### `ProjectCard`

Tarjeta individual de proyecto en la lista.

| Prop | Tipo | Descripción |
|------|------|-------------|
| `project` | `ProjectSummary` | Datos del proyecto con EVM consolidado |
| `onEdit` | `(project: ProjectSummary) => void` | Abrir modal de edición |
| `onDelete` | `(project: ProjectSummary) => void` | Abrir diálogo de eliminación |
| `onClick` | `(projectId: string) => void` | Navegar al dashboard |

**Muestra:** Nombre, descripción (truncada), total de actividades, BAC total, badges CPI y SPI.

### `ProjectModal`

Modal para crear o editar un proyecto.

| Prop | Tipo | Descripción |
|------|------|-------------|
| `open` | `boolean` | Controla visibilidad |
| `project` | `ProjectBase \| null` | `null` = crear, objeto = editar |
| `onSave` | `(data: ProjectCreate \| ProjectUpdate) => void` | Guardar |
| `onCancel` | `() => void` | Cerrar sin guardar |

**Campos:** Nombre (obligatorio), Descripción (opcional textarea).

---

## Componentes del dashboard

### `ProjectSelector`

Breadcrumb con dropdown para cambio rápido de proyecto.

| Prop | Tipo | Descripción |
|------|------|-------------|
| `currentProject` | `ProjectBase` | Proyecto actualmente visualizado |
| `projects` | `ProjectBase[]` | Lista de todos los proyectos |
| `onSelect` | `(projectId: string) => void` | Cambiar de proyecto |

### `EVMIndicators`

Panel con los 10 indicadores EVM consolidados del proyecto.

| Prop | Tipo | Descripción |
|------|------|-------------|
| `evm` | `EVMConsolidated` | Indicadores consolidados del proyecto |

**Muestra:** BAC total, PV, EV, AC, CV, SV, CPI (con badge), SPI (con badge), EAC, VAC. Cada indicador tiene tooltip con fórmula y descripción.

### `EVMChart`

Gráfica de barras agrupadas PV/EV/AC por actividad (Recharts).

| Prop | Tipo | Descripción |
|------|------|-------------|
| `activities` | `ActivityResponse[]` | Actividades con datos EVM |

**Ejes:** X = nombre de actividad, Y = valor monetario. Tres barras por actividad: PV (azul), EV (verde), AC (naranja). Incluye leyenda y tooltip.

### `ActivityTable`

Tabla de actividades con expansión progresiva.

| Prop | Tipo | Descripción |
|------|------|-------------|
| `activities` | `ActivityResponse[]` | Lista de actividades |
| `onEdit` | `(activity: ActivityResponse) => void` | Abrir modal de edición |
| `onDelete` | `(activity: ActivityResponse) => void` | Abrir diálogo de eliminación |

**Columnas:** Nombre, BAC, % Planificado, % Real, Costo Real, CPI (badge), SPI (badge), Acciones (✏️ 🗑️).

**Expansión:** Muestra las primeras 5 filas. Si hay más, muestra botón "Ver más (N restantes)" / "Ver menos".

### `ActivityModal`

Modal para crear o editar una actividad con vista previa EVM reactiva.

| Prop | Tipo | Descripción |
|------|------|-------------|
| `open` | `boolean` | Controla visibilidad |
| `activity` | `ActivityResponse \| null` | `null` = crear, objeto = editar |
| `onSave` | `(data: ActivityCreate \| ActivityUpdate) => void` | Guardar |
| `onCancel` | `() => void` | Cerrar sin guardar |

**Campos:** Nombre, BAC, % Planificado, % Real, Costo Real.

**Vista previa EVM:** Sección inferior del modal que muestra PV, EV, CPI, SPI recalculados en tiempo real usando `evmCalculator.ts` local (sin llamada al API).

---

## Utilidades

### `evmCalculator.ts`

Misma lógica EVM que el backend, para cálculo reactivo en el modal.

| Función | Entrada | Salida |
|---------|---------|--------|
| `calculateActivityEvm(bac, plannedPct, actualPct, actualCost)` | Datos numéricos | `EVMResult` con indicadores + estados + razones |

### `client.ts`

Instancia de Axios con `baseURL = http://localhost:8000/api/v1` y funciones tipadas por endpoint.

| Función | Método | Endpoint |
|---------|--------|----------|
| `getProjects()` | GET | `/projects` |
| `createProject(data)` | POST | `/projects` |
| `getProject(id)` | GET | `/projects/{id}` |
| `updateProject(id, data)` | PUT | `/projects/{id}` |
| `deleteProject(id)` | DELETE | `/projects/{id}` |
| `getActivities(projectId)` | GET | `/projects/{id}/activities` |
| `createActivity(projectId, data)` | POST | `/projects/{id}/activities` |
| `updateActivity(projectId, actId, data)` | PUT | `/projects/{id}/activities/{actId}` |
| `deleteActivity(projectId, actId)` | DELETE | `/projects/{id}/activities/{actId}` |

---

## Tipos (`types/evm.ts`)

```typescript
// Tipos principales que deben definirse
interface ProjectBase { id, name, description, created_at, updated_at }
interface ProjectSummary extends ProjectBase { total_actividades, evm_consolidado }
interface ProjectDetail extends ProjectBase { actividades, evm_consolidado }
interface ProjectCreate { name, description? }
interface ProjectUpdate { name?, description? }

interface ActivityCreate { name, bac, planned_percentage, actual_percentage, actual_cost }
interface ActivityUpdate { name?, bac?, planned_percentage?, actual_percentage?, actual_cost? }
interface ActivityResponse { id, project_id, name, bac, planned_percentage, actual_percentage, actual_cost, created_at, updated_at, evm }

interface EVMResult { pv, ev, cv, sv, cpi, spi, eac, vac, estado_cpi, estado_spi, razon_cpi, razon_spi }
interface EVMConsolidated extends EVMResult { bac_total, ac }

type EstadoCPI = 'bajo_presupuesto' | 'en_presupuesto' | 'sobre_presupuesto' | 'datos_insuficientes'
type EstadoSPI = 'adelantado' | 'en_cronograma' | 'atrasado' | 'datos_insuficientes'
type RazonEVM = 'costo_real_es_cero' | 'valor_planificado_es_cero' | null
```
