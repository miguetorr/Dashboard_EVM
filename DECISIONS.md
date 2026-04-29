# Registro de decisiones técnicas — EVM Tracker V1

Este documento registra las decisiones técnicas clave del proyecto, el razonamiento detrás de cada una, y las alternativas que se evaluaron. Es la referencia permanente de **por qué el proyecto está como está**.

---

## 1. Arquitectura: Capas con contratos explícitos

**Decisión**: Router → Service → Repository + EVM Calculator como módulo puro.

**Contexto**: Los requerimientos exigen que la lógica de negocio no viva en los controladores y que el código sea testeable.

**Alternativas evaluadas**:
- **MVC clásico**: Mezcla lógica en controladores. Descartado — los requerimientos lo prohíben explícitamente.
- **Hexagonal completa (puertos y adaptadores)**: Demasiada ceremonia para V1 con 2 entidades. Descartado por sobreingeniería.
- **Capas con interfaces explícitas**: Separación clara (Router/Service/Repository), cada capa se comunica vía contratos Pydantic, testeable de forma aislada. **Elegida**.

---

## 2. EVM Calculator: Funciones puras, no clases

**Decisión**: El motor de cálculo EVM son funciones puras sin estado ni dependencias externas.

**Razonamiento**: Los cálculos EVM son transformaciones `datos → datos`. No necesitan instanciación, no tienen estado, no hacen I/O. Una función `calculate_activity_evm(bac, planned_pct, actual_pct, actual_cost) → EVMResult` es la unidad mínima testeable.

**Alternativa descartada**: Clase `EVMCalculator` con métodos — agrega estado sin beneficio y complica el testing.

---

## 3. Indicadores EVM no se almacenan en base de datos

**Decisión**: Todos los valores EVM (PV, EV, CV, SV, CPI, SPI, EAC, VAC) se calculan en runtime. Nunca se persisten.

**Razonamiento**: Los indicadores son derivados de los datos almacenados. Persistirlos crearía riesgo de inconsistencia (actualizar un campo y olvidar recalcular). La DB es fuente de verdad de **hechos**, no de derivaciones.

**Compromiso aceptado**: Si hubiera miles de actividades por proyecto, el cálculo en runtime podría ser lento. Para V1 con volumen bajo, es irrelevante.

---

## 4. Consolidado por suma de componentes (estándar PMI)

**Decisión**: Los indicadores consolidados del proyecto se calculan sumando PV, EV y AC de todas las actividades primero, y luego calculando CPI y SPI sobre esas sumas.

**Alternativa descartada**: Promedio de los CPI/SPI individuales — matemáticamente incorrecto porque pondera igual actividades de presupuesto muy diferente ($100 vs $10,000).

---

## 5. Edge cases: null + razón descriptiva

**Decisión**: Cuando una división por cero impide el cálculo (CPI cuando AC=0, SPI cuando PV=0), el campo retorna `null` y un campo `razon_*` explica el motivo en español.

**Alternativas descartadas**:
- Retornar `0`: Engañoso — 0 tiene significado matemático diferente a "no calculable".
- Retornar `Infinity`: JSON no soporta Infinity de forma nativa.
- Lanzar excepción: No es un error — es un estado válido del dominio.

**Impacto en frontend**: Nunca se muestra `null` al usuario. Se muestra un badge con estado visual y la explicación ("No se puede calcular: el costo real es cero").

---

## 6. actual_cost >= 0 (no > 0)

**Decisión**: El costo real admite el valor 0.

**Razonamiento**: Una actividad recién creada puede no tener costo incurrido todavía. Forzar un costo positivo obligaría a registrar un valor falso. El edge case AC=0 se maneja con `null` + razón en los indicadores que dependen de AC.

---

## 7. cut_off_date implícita (sin campo en DB)

**Decisión**: No existe un campo `cut_off_date` en la base de datos. La fecha de corte es implícita — es el momento en que el usuario registra el porcentaje de avance planificado.

**Razonamiento**: Los requerimientos no definen explícitamente este campo, y el dato del porcentaje planificado ya captura la información necesaria sin complejidad adicional.

---

## 8. Sin autenticación en V1, preparada para V2

**Decisión**: V1 no tiene auth. Todos los usuarios ven todos los proyectos.

**Preparación para V2**: Los services reciben un parámetro `principal` que en V1 es un `AnonymousPrincipal` (autoriza todo). En V2 se reemplaza por `AuthenticatedPrincipal` sin cambiar firmas de servicio ni contratos.

---

## 9. Hard delete (sin soft delete)

**Decisión**: La eliminación de proyectos y actividades es permanente (hard delete con CASCADE en DB).

**Razonamiento**: V1 es herramienta interna con datos de ejemplo. No se requiere historial ni recuperación. Se mitiga con diálogos de confirmación obligatorios en el frontend.

**V2**: Evaluar soft delete si se requiere auditoría o recuperación.

---

## 10. Cálculo reactivo en cliente

**Decisión**: El frontend recalcula indicadores EVM localmente mientras el usuario edita los campos, sin esperar una petición HTTP. Al guardar, el backend confirma.

**Alternativas descartadas**:
- API call en cada keypress: costoso e innecesario.
- WebSockets: complejidad arquitectónica injustificada para V1.

**Compromiso**: La lógica EVM se duplica en backend (Python) y frontend (TypeScript). La lógica frontend es solo para preview — el backend es la fuente de verdad. Los tests cubren ambas implementaciones.

---

## 11. Validación en dos capas

**Decisión**: Las validaciones de datos se aplican tanto en Pydantic (capa API, feedback inmediato al usuario) como en CHECK constraints de PostgreSQL (capa DB, integridad garantizada).

**Constraints en DB**:
- `bac > 0`
- `actual_cost >= 0`
- `planned_percentage BETWEEN 0 AND 100`
- `actual_percentage BETWEEN 0 AND 100`

**Razonamiento**: Si alguien hace un INSERT directo a la DB saltándose la API, las CHECK constraints lo frenan. Defensa en profundidad.

---

## 12. Versionado de API desde V1

**Decisión**: Prefijo `/api/v1/` en todos los endpoints desde el inicio.

**Razonamiento**: Cuando exista V2 (con auth, nuevas funcionalidades), los endpoints V1 siguen funcionando. Costo cero implementarlo ahora, costo alto no tenerlo después.

---

## 13. Sin migraciones en V1

**Decisión**: No se usa Alembic ni herramienta de migraciones. El esquema se define vía script DDL manual.

**Razonamiento**: V1 es un deploy inicial sin datos en producción que preservar. Alembic agrega complejidad al setup sin beneficio inmediato.

**V2**: Incorporar Alembic cuando haya datos reales y el esquema pueda evolucionar.

---

## 14. Recharts para gráficas

**Decisión**: Recharts como librería de visualización.

**Alternativas evaluadas**:
- Chart.js + react-chartjs-2: Más pesada, API imperativa.
- D3: Excesivo para gráficas de barras simples.
- Recharts: Ligera, declarativa, API nativa de React, bien mantenida. **Elegida**.

---

## 15. Todos los textos y estados en español

**Decisión**: Los estados de CPI/SPI (`bajo_presupuesto`, `sobre_presupuesto`, `adelantado`, `atrasado`, `datos_insuficientes`) y las razones (`costo_real_es_cero`, `valor_planificado_es_cero`) se retornan en español desde el backend.

**Razonamiento**: La aplicación es de uso interno, todos los usuarios son hispanohablantes, no se contempla internacionalización.
