## ADDED Requirements

### Requirement: Lista de proyectos
El frontend SHALL mostrar una página con todos los proyectos en formato de tarjetas (cards), cada una mostrando nombre, descripción, conteo de actividades, BAC total, y estado visual de CPI y SPI.

#### Scenario: Visualización de tarjetas de proyecto
- **WHEN** el usuario navega a `/projects`
- **THEN** ve las tarjetas de todos los proyectos con indicadores CPI y SPI con badges de color (🟢 favorable, 🟡 neutral, 🔴 desfavorable, ⚪ datos insuficientes)

#### Scenario: No existen proyectos
- **WHEN** no hay proyectos registrados
- **THEN** se muestra un estado vacío con mensaje invitando a crear el primer proyecto

### Requirement: Crear proyecto desde la lista
El frontend SHALL mostrar un botón "Nuevo" que abre un modal para crear un proyecto con nombre y descripción.

#### Scenario: Crear proyecto exitosamente
- **WHEN** el usuario presiona "Nuevo", completa el nombre y presiona "Guardar"
- **THEN** el modal se cierra, la lista se actualiza mostrando el nuevo proyecto

#### Scenario: Cancelar creación
- **WHEN** el usuario presiona "Cancelar" en el modal
- **THEN** el modal se cierra sin crear nada

### Requirement: Editar proyecto desde la lista
El frontend SHALL permitir editar nombre y descripción de un proyecto mediante un botón de edición en cada tarjeta que abre un modal.

#### Scenario: Editar proyecto exitosamente
- **WHEN** el usuario presiona ✏️ en una tarjeta, modifica el nombre y presiona "Guardar"
- **THEN** el modal se cierra y la tarjeta refleja los cambios

### Requirement: Eliminar proyecto con confirmación
El frontend SHALL mostrar un botón de eliminación en cada tarjeta que abre un diálogo de confirmación mostrando el nombre del proyecto y el conteo de actividades que se eliminarán.

#### Scenario: Confirmar eliminación
- **WHEN** el usuario presiona 🗑️, ve el diálogo "¿Desea eliminar el proyecto X? Se eliminarán N actividades. Esta acción no se puede deshacer." y presiona "Eliminar"
- **THEN** el proyecto y sus actividades se eliminan, la lista se actualiza

#### Scenario: Cancelar eliminación
- **WHEN** el usuario presiona "Cancelar" en el diálogo
- **THEN** nada se elimina

### Requirement: Dashboard de proyecto
El frontend SHALL mostrar una vista de dashboard al seleccionar un proyecto, con indicadores consolidados, tabla de actividades, y gráfica comparativa.

#### Scenario: Navegación al dashboard
- **WHEN** el usuario hace click en una tarjeta de proyecto
- **THEN** navega a `/projects/:id` con el dashboard completo

### Requirement: Selector rápido de proyecto
El frontend SHALL incluir un breadcrumb con dropdown para cambiar de proyecto sin navegar atrás a la lista.

#### Scenario: Cambiar de proyecto desde el dashboard
- **WHEN** el usuario hace click en el dropdown del breadcrumb y selecciona otro proyecto
- **THEN** el dashboard se actualiza con los datos del proyecto seleccionado sin navegación intermedia

### Requirement: Indicadores consolidados
El frontend SHALL mostrar los indicadores EVM consolidados del proyecto (BAC total, PV, EV, AC, CV, SV, CPI, SPI, EAC, VAC) con badges de color para CPI y SPI.

#### Scenario: Indicadores con datos suficientes
- **WHEN** el proyecto tiene actividades con datos completos
- **THEN** se muestran todos los indicadores con colores: 🟢 para favorable (CPI/SPI > 1), 🟡 para neutral (= 1), 🔴 para desfavorable (< 1)

#### Scenario: Indicadores con datos insuficientes
- **WHEN** un indicador es null (ej. CPI porque AC total = 0)
- **THEN** se muestra un badge ⚪ con texto descriptivo (ej. "No se puede calcular: el costo real es cero") en lugar del número

### Requirement: Tabla de actividades con expansión
El frontend SHALL mostrar las primeras 5 actividades en una tabla con sus indicadores EVM. Si hay más de 5, un botón "Ver más (N actividades restantes)" expande el resto.

#### Scenario: Menos de 5 actividades
- **WHEN** el proyecto tiene 3 actividades
- **THEN** se muestran las 3 en la tabla sin botón de expansión

#### Scenario: Más de 5 actividades
- **WHEN** el proyecto tiene 8 actividades
- **THEN** se muestran las primeras 5 con un botón "Ver más (3 actividades restantes)"

#### Scenario: Expandir actividades
- **WHEN** el usuario presiona "Ver más"
- **THEN** se muestran todas las actividades y el botón cambia a "Ver menos"

### Requirement: CRUD de actividades con modal
El frontend SHALL permitir crear y editar actividades mediante un modal con campos: nombre, BAC, porcentaje planificado, porcentaje real y costo real. El modal incluye una vista previa reactiva de los indicadores EVM.

#### Scenario: Crear actividad
- **WHEN** el usuario presiona "Nueva actividad", completa los campos y presiona "Guardar"
- **THEN** la actividad se crea, la tabla y los indicadores consolidados se actualizan

#### Scenario: Editar actividad
- **WHEN** el usuario presiona ✏️ en una fila, modifica campos en el modal y presiona "Guardar"
- **THEN** la actividad se actualiza, la tabla y los indicadores consolidados se actualizan

#### Scenario: Vista previa reactiva en modal
- **WHEN** el usuario modifica un campo numérico en el modal de actividad
- **THEN** los indicadores CPI y SPI en la sección "Vista previa EVM" se recalculan instantáneamente sin llamar al API

### Requirement: Eliminar actividad con confirmación
El frontend SHALL mostrar un botón 🗑️ en cada fila de actividad que abre un diálogo confirmando el nombre de la actividad a eliminar.

#### Scenario: Confirmar eliminación de actividad
- **WHEN** el usuario presiona 🗑️ en una fila, ve "¿Desea eliminar la actividad X? Esta acción no se puede deshacer." y presiona "Eliminar"
- **THEN** la actividad se elimina, la tabla y los indicadores consolidados se actualizan

### Requirement: Gráfica comparativa PV/EV/AC
El frontend SHALL mostrar una gráfica de barras agrupadas que compare PV, EV y AC por cada actividad del proyecto.

#### Scenario: Gráfica con actividades
- **WHEN** el proyecto tiene actividades con datos
- **THEN** se muestra un gráfico de barras agrupadas con tres barras por actividad (PV, EV, AC) con leyenda

#### Scenario: Gráfica sin actividades
- **WHEN** el proyecto no tiene actividades
- **THEN** se muestra un estado vacío en el área de la gráfica

### Requirement: Glosario EVM
El frontend SHALL incluir un panel colapsable con la explicación en español de cada indicador EVM, accesible desde el dashboard.

#### Scenario: Ver glosario
- **WHEN** el usuario presiona "¿Qué significan estos indicadores?"
- **THEN** se expande un panel con las definiciones de BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC, VAC en lenguaje claro para no expertos

### Requirement: Tooltips en indicadores
El frontend SHALL mostrar un tooltip al pasar el mouse sobre cada indicador, con la fórmula de cálculo y una descripción breve.

#### Scenario: Tooltip sobre CPI
- **WHEN** el usuario pasa el mouse sobre el valor de CPI
- **THEN** se muestra un tooltip con "CPI = EV / AC — Índice de rendimiento de costo. Mayor a 1 = eficiente."
