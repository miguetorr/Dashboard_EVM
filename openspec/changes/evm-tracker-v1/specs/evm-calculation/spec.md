## ADDED Requirements

### Requirement: Cálculo de indicadores EVM por actividad
El sistema SHALL calcular los 8 indicadores EVM para cada actividad a partir de sus datos registrados (bac, planned_percentage, actual_percentage, actual_cost).

#### Scenario: Cálculo estándar con todos los datos válidos
- **WHEN** una actividad tiene bac=10000, planned_percentage=60, actual_percentage=40, actual_cost=7000
- **THEN** el sistema calcula: PV=6000, EV=4000, CV=-3000, SV=-2000, CPI=0.5714, SPI=0.6667, EAC=17500, VAC=-7500

#### Scenario: Actividad con avance completo y en presupuesto
- **WHEN** una actividad tiene bac=5000, planned_percentage=100, actual_percentage=100, actual_cost=5000
- **THEN** el sistema calcula: PV=5000, EV=5000, CV=0, SV=0, CPI=1.0, SPI=1.0, EAC=5000, VAC=0

#### Scenario: Actividad sin avance planificado (PV=0)
- **WHEN** una actividad tiene planned_percentage=0
- **THEN** PV=0, SPI=null con razon_spi="valor_planificado_es_cero"

#### Scenario: Actividad sin costo real (AC=0)
- **WHEN** una actividad tiene actual_cost=0
- **THEN** CPI=null con razon_cpi="costo_real_es_cero", EAC=null, VAC=null

#### Scenario: Actividad sin avance real (actual_percentage=0)
- **WHEN** una actividad tiene actual_percentage=0 y actual_cost=5000
- **THEN** EV=0, CV=-5000, CPI=0, SPI=0 (o null si PV también es 0), EAC=infinito conceptual → null con razón

#### Scenario: Avance real y planificado ambos en cero
- **WHEN** una actividad tiene planned_percentage=0 y actual_percentage=0 y actual_cost=0
- **THEN** PV=0, EV=0, CV=0, SV=0, CPI=null, SPI=null, EAC=null, VAC=null con estado "datos_insuficientes"

### Requirement: Cálculo consolidado por proyecto
El sistema SHALL calcular los indicadores EVM consolidados del proyecto usando suma de componentes: se suman PV, EV y AC de todas las actividades primero, y luego se calculan los índices sobre esas sumas. El BAC total es la suma de BAC de todas las actividades.

#### Scenario: Consolidado con múltiples actividades
- **WHEN** un proyecto tiene actividad A (PV=6000, EV=4000, AC=7000) y actividad B (PV=10000, EV=6000, AC=8000)
- **THEN** el consolidado calcula: PV_total=16000, EV_total=10000, AC_total=15000, CPI=10000/15000=0.6667, SPI=10000/16000=0.625

#### Scenario: Consolidado sin actividades
- **WHEN** un proyecto no tiene actividades
- **THEN** todos los indicadores consolidados son 0 o null según corresponda

#### Scenario: Consolidado con todas las actividades sin costo
- **WHEN** todas las actividades tienen actual_cost=0
- **THEN** AC_total=0, CPI_total=null con razon_cpi="costo_real_es_cero"

### Requirement: Interpretación de CPI
El sistema SHALL retornar el estado interpretado del CPI en español.

#### Scenario: CPI mayor a 1
- **WHEN** CPI > 1
- **THEN** estado_cpi = "bajo_presupuesto" (el proyecto gasta menos de lo que avanza)

#### Scenario: CPI igual a 1
- **WHEN** CPI = 1
- **THEN** estado_cpi = "en_presupuesto"

#### Scenario: CPI menor a 1
- **WHEN** CPI < 1
- **THEN** estado_cpi = "sobre_presupuesto" (se gasta más de lo que se avanza)

#### Scenario: CPI no calculable
- **WHEN** CPI es null
- **THEN** estado_cpi = "datos_insuficientes"

### Requirement: Interpretación de SPI
El sistema SHALL retornar el estado interpretado del SPI en español.

#### Scenario: SPI mayor a 1
- **WHEN** SPI > 1
- **THEN** estado_spi = "adelantado"

#### Scenario: SPI igual a 1
- **WHEN** SPI = 1
- **THEN** estado_spi = "en_cronograma"

#### Scenario: SPI menor a 1
- **WHEN** SPI < 1
- **THEN** estado_spi = "atrasado"

#### Scenario: SPI no calculable
- **WHEN** SPI es null
- **THEN** estado_spi = "datos_insuficientes"

### Requirement: Precisión numérica
El sistema SHALL redondear los índices (CPI, SPI) a 4 decimales y los valores monetarios (PV, EV, CV, SV, EAC, VAC) a 2 decimales.

#### Scenario: Redondeo de CPI
- **WHEN** EV=4000 y AC=7000
- **THEN** CPI = 0.5714 (redondeado a 4 decimales)

#### Scenario: Redondeo de valores monetarios
- **WHEN** BAC=10000, CPI=0.5714
- **THEN** EAC = 17501.75 (redondeado a 2 decimales)
