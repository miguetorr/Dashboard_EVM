## ADDED Requirements

### Requirement: Tabla projects
La base de datos SHALL tener una tabla `projects` con columnas: id (UUID, PK, default gen_random_uuid()), name (VARCHAR(255), NOT NULL), description (TEXT, nullable), created_at (TIMESTAMPTZ, NOT NULL, default NOW()), updated_at (TIMESTAMPTZ, NOT NULL, default NOW()).

#### Scenario: Crear tabla projects
- **WHEN** se ejecuta el DDL de la tabla projects
- **THEN** la tabla se crea con todas las columnas, tipos y defaults especificados

### Requirement: Tabla activities
La base de datos SHALL tener una tabla `activities` con columnas: id (UUID, PK, default gen_random_uuid()), project_id (UUID, FK a projects.id, NOT NULL, ON DELETE CASCADE), name (VARCHAR(255), NOT NULL), bac (DECIMAL(15,2), NOT NULL), planned_percentage (DECIMAL(5,2), NOT NULL), actual_percentage (DECIMAL(5,2), NOT NULL), actual_cost (DECIMAL(15,2), NOT NULL), created_at (TIMESTAMPTZ, NOT NULL, default NOW()), updated_at (TIMESTAMPTZ, NOT NULL, default NOW()).

#### Scenario: Crear tabla activities
- **WHEN** se ejecuta el DDL de la tabla activities
- **THEN** la tabla se crea con todas las columnas, tipos, foreign key y defaults especificados

### Requirement: Constraint BAC positivo
La base de datos SHALL rechazar INSERT y UPDATE en activities cuando bac sea menor o igual a 0.

#### Scenario: Insert con BAC positivo
- **WHEN** se inserta una actividad con bac = 10000
- **THEN** el insert se ejecuta exitosamente

#### Scenario: Insert con BAC cero
- **WHEN** se inserta una actividad con bac = 0
- **THEN** la base de datos rechaza el insert con error de CHECK constraint

#### Scenario: Insert con BAC negativo
- **WHEN** se inserta una actividad con bac = -500
- **THEN** la base de datos rechaza el insert con error de CHECK constraint

### Requirement: Constraint actual_cost no negativo
La base de datos SHALL rechazar INSERT y UPDATE en activities cuando actual_cost sea menor a 0. El valor 0 es permitido.

#### Scenario: Insert con actual_cost cero
- **WHEN** se inserta una actividad con actual_cost = 0
- **THEN** el insert se ejecuta exitosamente

#### Scenario: Insert con actual_cost negativo
- **WHEN** se inserta una actividad con actual_cost = -100
- **THEN** la base de datos rechaza el insert con error de CHECK constraint

### Requirement: Constraint porcentajes en rango 0-100
La base de datos SHALL rechazar INSERT y UPDATE en activities cuando planned_percentage o actual_percentage estén fuera del rango 0 a 100 (inclusive).

#### Scenario: Insert con porcentaje en rango
- **WHEN** se inserta con planned_percentage = 50 y actual_percentage = 30
- **THEN** el insert se ejecuta exitosamente

#### Scenario: Insert con porcentaje negativo
- **WHEN** se inserta con planned_percentage = -5
- **THEN** la base de datos rechaza el insert con error de CHECK constraint

#### Scenario: Insert con porcentaje mayor a 100
- **WHEN** se inserta con actual_percentage = 101
- **THEN** la base de datos rechaza el insert con error de CHECK constraint

### Requirement: Cascade delete
La base de datos SHALL eliminar automáticamente todas las actividades de un proyecto cuando el proyecto es eliminado.

#### Scenario: Eliminar proyecto con actividades
- **WHEN** se elimina un proyecto que tiene 3 actividades
- **THEN** el proyecto y sus 3 actividades se eliminan de la base de datos

### Requirement: Script seed con datos de ejemplo
El entregable SHALL incluir un script SQL con datos de ejemplo que inserte al menos 2 proyectos con al menos 3 actividades cada uno, cubriendo escenarios variados (proyecto en buen estado, proyecto en mal estado, actividades con AC=0).

#### Scenario: Ejecutar seed
- **WHEN** se ejecuta el script seed sobre una base de datos con el DDL aplicado
- **THEN** se insertan los proyectos y actividades de ejemplo sin errores
