## ADDED Requirements

### Requirement: Crear actividad
El sistema SHALL permitir crear una actividad dentro de un proyecto proporcionando name, bac, planned_percentage, actual_percentage y actual_cost.

#### Scenario: Creación exitosa
- **WHEN** se envía POST `/api/v1/projects/{project_id}/activities` con `{"name": "Diseño UI", "bac": 10000, "planned_percentage": 60, "actual_percentage": 40, "actual_cost": 7000}`
- **THEN** el sistema retorna 201 con la actividad creada incluyendo id (UUID), todos los campos enviados, y el bloque evm calculado

#### Scenario: Creación con actividad sin costo (edge case AC=0)
- **WHEN** se envía POST con `{"name": "Fase inicial", "bac": 5000, "planned_percentage": 20, "actual_percentage": 10, "actual_cost": 0}`
- **THEN** el sistema retorna 201 con la actividad creada y evm.cpi como null con razon_cpi "costo_real_es_cero"

#### Scenario: BAC menor o igual a cero
- **WHEN** se envía POST con bac = 0 o bac negativo
- **THEN** el sistema retorna 422 con mensaje indicando que el presupuesto (BAC) debe ser mayor a cero

#### Scenario: Actual cost negativo
- **WHEN** se envía POST con actual_cost negativo
- **THEN** el sistema retorna 422 con mensaje indicando que el costo real no puede ser negativo

#### Scenario: Porcentaje fuera de rango
- **WHEN** se envía POST con planned_percentage o actual_percentage menor a 0 o mayor a 100
- **THEN** el sistema retorna 422 con mensaje indicando que el porcentaje debe estar entre 0 y 100

#### Scenario: Proyecto inexistente
- **WHEN** se envía POST `/api/v1/projects/{project_id}/activities` con un project_id que no existe
- **THEN** el sistema retorna 404 con mensaje "Proyecto no encontrado"

### Requirement: Listar actividades de un proyecto
El sistema SHALL retornar todas las actividades de un proyecto con sus indicadores EVM calculados.

#### Scenario: Proyecto con actividades
- **WHEN** se envía GET `/api/v1/projects/{project_id}/activities`
- **THEN** el sistema retorna 200 con un array de actividades, cada una con sus datos base y su bloque evm

#### Scenario: Proyecto sin actividades
- **WHEN** se envía GET `/api/v1/projects/{project_id}/activities` y el proyecto no tiene actividades
- **THEN** el sistema retorna 200 con un array vacío

### Requirement: Editar actividad
El sistema SHALL permitir editar cualquier campo registrable de una actividad existente.

#### Scenario: Edición exitosa
- **WHEN** se envía PUT `/api/v1/projects/{project_id}/activities/{activity_id}` con campos actualizados
- **THEN** el sistema retorna 200 con la actividad actualizada, indicadores EVM recalculados, y updated_at modificado

#### Scenario: Edición con validaciones violadas
- **WHEN** se envía PUT con bac = -100 o actual_percentage = 150
- **THEN** el sistema retorna 422 con mensaje de validación correspondiente

#### Scenario: Actividad inexistente
- **WHEN** se envía PUT con un activity_id que no existe
- **THEN** el sistema retorna 404 con mensaje "Actividad no encontrada"

### Requirement: Eliminar actividad
El sistema SHALL permitir eliminar una actividad existente de forma permanente.

#### Scenario: Eliminación exitosa
- **WHEN** se envía DELETE `/api/v1/projects/{project_id}/activities/{activity_id}`
- **THEN** el sistema retorna 204 y la actividad es eliminada permanentemente

#### Scenario: Actividad inexistente
- **WHEN** se envía DELETE con un activity_id que no existe
- **THEN** el sistema retorna 404 con mensaje "Actividad no encontrada"

### Requirement: Validación de porcentaje real mayor a 100
El sistema SHALL rechazar valores de actual_percentage mayores a 100 y retornar un mensaje claro de advertencia.

#### Scenario: Porcentaje real exactamente 100
- **WHEN** se envía actual_percentage = 100
- **THEN** el sistema acepta el valor normalmente

#### Scenario: Porcentaje real mayor a 100
- **WHEN** se envía actual_percentage = 105
- **THEN** el sistema retorna 422 con mensaje "El porcentaje real no puede superar el 100%"
