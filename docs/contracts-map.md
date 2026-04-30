# Mapa de contratos — EVM Tracker API v1

Referencia rápida de la forma (shape) de cada request y response. Para el detalle completo con validaciones, enums, y ejemplos, consultar `openapi.yaml`.

---

## Proyectos

### `GET /api/v1/projects` — Listar proyectos

**Response 200** — `Array<ProyectoResumen>`

```json
[
  {
    "id": "uuid",
    "name": "string",
    "description": "string | null",
    "created_at": "datetime",
    "updated_at": "datetime",
    "total_actividades": 3,
    "evm_consolidado": {
      "bac_total": 50000.00,
      "pv": 30000.00,
      "ev": 20000.00,
      "ac": 35000.00,
      "cv": -15000.00,
      "sv": -10000.00,
      "cpi": 0.5714,
      "spi": 0.6667,
      "eac": 87500.00,
      "vac": -37500.00,
      "estado_cpi": "sobre_presupuesto",
      "estado_spi": "atrasado",
      "razon_cpi": null,
      "razon_spi": null
    }
  }
]
```

---

### `POST /api/v1/projects` — Crear proyecto

**Request Body** — `ProyectoCrear`

```json
{
  "name": "string (obligatorio, 1-255 chars)",
  "description": "string | null (opcional)"
}
```

**Response 201** — `ProyectoBase`

```json
{
  "id": "uuid",
  "name": "string",
  "description": "string | null",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Errores**: `422` validación (nombre vacío o ausente)

---

### `GET /api/v1/projects/{project_id}` — Detalle de proyecto

**Response 200** — `ProyectoDetalle`

```json
{
  "id": "uuid",
  "name": "string",
  "description": "string | null",
  "created_at": "datetime",
  "updated_at": "datetime",
  "actividades": [
    {
      "id": "uuid",
      "project_id": "uuid",
      "name": "string",
      "bac": 10000.00,
      "planned_percentage": 60.00,
      "actual_percentage": 40.00,
      "actual_cost": 7000.00,
      "created_at": "datetime",
      "updated_at": "datetime",
      "evm": { "...EVMActividad" }
    }
  ],
  "evm_consolidado": { "...EVMConsolidado" }
}
```

**Errores**: `404` proyecto no encontrado

---

### `PUT /api/v1/projects/{project_id}` — Editar proyecto

**Request Body** — `ProyectoEditar` (campos opcionales)

```json
{
  "name": "string (1-255 chars, opcional)",
  "description": "string | null (opcional)"
}
```

**Response 200** — `ProyectoBase`

**Errores**: `404` no encontrado, `422` validación

---

### `DELETE /api/v1/projects/{project_id}` — Eliminar proyecto

**Response 204** — Sin cuerpo (cascade: elimina proyecto + todas sus actividades)

**Errores**: `404` proyecto no encontrado

---

## Actividades

### `GET /api/v1/projects/{project_id}/activities` — Listar actividades

**Response 200** — `Array<ActividadRespuesta>`

```json
[
  {
    "id": "uuid",
    "project_id": "uuid",
    "name": "string",
    "bac": 10000.00,
    "planned_percentage": 60.00,
    "actual_percentage": 40.00,
    "actual_cost": 7000.00,
    "created_at": "datetime",
    "updated_at": "datetime",
    "evm": {
      "pv": 6000.00,
      "ev": 4000.00,
      "cv": -3000.00,
      "sv": -2000.00,
      "cpi": 0.5714,
      "spi": 0.6667,
      "eac": 17500.00,
      "vac": -7500.00,
      "estado_cpi": "sobre_presupuesto",
      "estado_spi": "atrasado",
      "razon_cpi": null,
      "razon_spi": null
    }
  }
]
```

**Errores**: `404` proyecto no encontrado

---

### `POST /api/v1/projects/{project_id}/activities` — Crear actividad

**Request Body** — `ActividadCrear`

```json
{
  "name": "string (obligatorio, 1-255 chars)",
  "bac": "number (obligatorio, > 0)",
  "planned_percentage": "number (obligatorio, 0-100)",
  "actual_percentage": "number (obligatorio, 0-100)",
  "actual_cost": "number (obligatorio, >= 0)"
}
```

**Response 201** — `ActividadRespuesta` (incluye bloque `evm` calculado)

**Errores**: `404` proyecto no encontrado, `422` validación (BAC ≤ 0, AC < 0, porcentaje fuera de rango)

---

### `PUT /api/v1/projects/{project_id}/activities/{activity_id}` — Editar actividad

**Request Body** — `ActividadEditar` (todos opcionales)

```json
{
  "name": "string (1-255 chars)",
  "bac": "number (> 0)",
  "planned_percentage": "number (0-100)",
  "actual_percentage": "number (0-100)",
  "actual_cost": "number (>= 0)"
}
```

**Response 200** — `ActividadRespuesta` (EVM recalculado)

**Errores**: `404` no encontrada, `422` validación

---

### `DELETE /api/v1/projects/{project_id}/activities/{activity_id}` — Eliminar actividad

**Response 204** — Sin cuerpo

**Errores**: `404` actividad no encontrada

---

## Shapes compartidos

### EVMActividad

```json
{
  "pv": "number (2 decimales)",
  "ev": "number (2 decimales)",
  "cv": "number (2 decimales)",
  "sv": "number (2 decimales)",
  "cpi": "number | null (4 decimales)",
  "spi": "number | null (4 decimales)",
  "eac": "number | null (2 decimales)",
  "vac": "number | null (2 decimales)",
  "estado_cpi": "bajo_presupuesto | en_presupuesto | sobre_presupuesto | datos_insuficientes",
  "estado_spi": "adelantado | en_cronograma | atrasado | datos_insuficientes",
  "razon_cpi": "costo_real_es_cero | null",
  "razon_spi": "valor_planificado_es_cero | null"
}
```

### EVMConsolidado

Igual que EVMActividad pero con campo adicional:

```json
{
  "bac_total": "number (2 decimales)",
  "ac": "number (2 decimales)",
  "...resto igual que EVMActividad"
}
```

### ErrorValidacion (formato FastAPI/Pydantic)

```json
{
  "detail": [
    {
      "loc": ["body", "bac"],
      "msg": "El presupuesto (BAC) debe ser mayor a cero",
      "type": "value_error"
    }
  ]
}
```

### ErrorNotFound

```json
{
  "detail": "Proyecto no encontrado"
}
```

---

## Códigos HTTP usados

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| 200 | OK | GET exitoso, PUT exitoso |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 404 | Not Found | Recurso no existe |
| 422 | Unprocessable Entity | Validación fallida |
