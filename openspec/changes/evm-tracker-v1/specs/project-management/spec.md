## ADDED Requirements

### Requirement: Crear proyecto
El sistema SHALL permitir crear un proyecto proporcionando nombre (obligatorio) y descripción (opcional).

#### Scenario: Creación exitosa con nombre y descripción
- **WHEN** se envía POST `/api/v1/projects` con `{"name": "Rediseño Portal", "description": "Actualización del portal corporativo"}`
- **THEN** el sistema retorna 201 con el proyecto creado incluyendo id (UUID), name, description, created_at y updated_at

#### Scenario: Creación exitosa sin descripción
- **WHEN** se envía POST `/api/v1/projects` con `{"name": "App Móvil"}`
- **THEN** el sistema retorna 201 con el proyecto creado y description como null

#### Scenario: Creación sin nombre
- **WHEN** se envía POST `/api/v1/projects` con `{}` o con name vacío
- **THEN** el sistema retorna 422 con mensaje de validación indicando que el nombre es obligatorio

### Requirement: Listar proyectos
El sistema SHALL retornar la lista de todos los proyectos con resumen de actividades e indicadores consolidados.

#### Scenario: Listar proyectos existentes
- **WHEN** se envía GET `/api/v1/projects` y existen proyectos
- **THEN** el sistema retorna 200 con un array de proyectos, cada uno con id, name, description, conteo de actividades, e indicadores EVM consolidados (bac_total, pv, ev, ac, cpi, spi, estado_cpi, estado_spi)

#### Scenario: Listar sin proyectos
- **WHEN** se envía GET `/api/v1/projects` y no existen proyectos
- **THEN** el sistema retorna 200 con un array vacío

### Requirement: Ver detalle de proyecto
El sistema SHALL retornar un proyecto con todas sus actividades y los indicadores EVM calculados por actividad y consolidados por proyecto.

#### Scenario: Proyecto existente con actividades
- **WHEN** se envía GET `/api/v1/projects/{project_id}` y el proyecto tiene actividades
- **THEN** el sistema retorna 200 con el proyecto, su lista de actividades (cada una con su bloque evm calculado), y el bloque evm_consolidado del proyecto

#### Scenario: Proyecto existente sin actividades
- **WHEN** se envía GET `/api/v1/projects/{project_id}` y el proyecto no tiene actividades
- **THEN** el sistema retorna 200 con el proyecto, lista de actividades vacía, y evm_consolidado con todos los valores en 0 o null según corresponda

#### Scenario: Proyecto inexistente
- **WHEN** se envía GET `/api/v1/projects/{project_id}` con un UUID que no existe
- **THEN** el sistema retorna 404 con mensaje "Proyecto no encontrado"

### Requirement: Editar proyecto
El sistema SHALL permitir editar el nombre y/o descripción de un proyecto existente.

#### Scenario: Edición exitosa
- **WHEN** se envía PUT `/api/v1/projects/{project_id}` con `{"name": "Nombre nuevo"}`
- **THEN** el sistema retorna 200 con el proyecto actualizado y updated_at modificado

#### Scenario: Editar proyecto inexistente
- **WHEN** se envía PUT `/api/v1/projects/{project_id}` con un UUID que no existe
- **THEN** el sistema retorna 404 con mensaje "Proyecto no encontrado"

### Requirement: Eliminar proyecto
El sistema SHALL permitir eliminar un proyecto y todas sus actividades asociadas (cascade delete).

#### Scenario: Eliminación exitosa
- **WHEN** se envía DELETE `/api/v1/projects/{project_id}` de un proyecto existente con actividades
- **THEN** el sistema retorna 204, el proyecto y todas sus actividades son eliminados permanentemente de la base de datos

#### Scenario: Eliminar proyecto inexistente
- **WHEN** se envía DELETE `/api/v1/projects/{project_id}` con un UUID que no existe
- **THEN** el sistema retorna 404 con mensaje "Proyecto no encontrado"
