# Diseño de datos semilla — EVM Tracker v1

Define los datos de ejemplo que irán en `sql/seed.sql`. Cubren escenarios variados para que el evaluador pueda probar el dashboard inmediatamente sin cargar datos manualmente.

---

## Criterios de diseño

1. **Mínimo 2 proyectos** con al menos 3 actividades cada uno (requisito del enunciado)
2. **Escenarios variados**: proyecto sano, proyecto con problemas, edge cases
3. **Datos realistas**: nombres y montos plausibles para un contexto de gestión de proyectos
4. **Edge cases cubiertos**: actividad con AC=0, actividad con avance planificado=0, proyecto sin desvíos
5. **Todos los estados EVM representados**: bajo_presupuesto, sobre_presupuesto, en_presupuesto, adelantado, atrasado, datos_insuficientes

---

## Proyecto 1: "Rediseño Portal Web"

**Narrativa**: Proyecto en problemas — va retrasado y por encima del presupuesto.

| Actividad | BAC | % Plan | % Real | AC | CPI esperado | SPI esperado | Estado |
|-----------|-----|--------|--------|----|-------------|-------------|--------|
| Diseño UI/UX | 15,000 | 100 | 100 | 18,000 | 0.8333 | 1.0 | Sobre presupuesto, en cronograma |
| Desarrollo Frontend | 25,000 | 60 | 40 | 18,000 | 0.5556 | 0.6667 | Sobre presupuesto, atrasado |
| Desarrollo Backend | 20,000 | 50 | 35 | 12,000 | 0.5833 | 0.7 | Sobre presupuesto, atrasado |
| Testing QA | 10,000 | 30 | 10 | 5,000 | 0.2 | 0.3333 | Sobre presupuesto, atrasado |

**Consolidado esperado**: BAC_total=70,000, CPI < 1, SPI < 1 → proyecto en rojo en ambos indicadores.

---

## Proyecto 2: "App Móvil Inventarios"

**Narrativa**: Proyecto saludable — va adelantado y dentro de presupuesto.

| Actividad | BAC | % Plan | % Real | AC | CPI esperado | SPI esperado | Estado |
|-----------|-----|--------|--------|----|-------------|-------------|--------|
| Arquitectura y diseño | 8,000 | 100 | 100 | 7,500 | 1.0667 | 1.0 | Bajo presupuesto, en cronograma |
| Módulo de inventario | 18,000 | 70 | 80 | 11,000 | 1.3091 | 1.1429 | Bajo presupuesto, adelantado |
| Módulo de reportes | 12,000 | 40 | 50 | 4,500 | 1.3333 | 1.25 | Bajo presupuesto, adelantado |
| Integración API externa | 6,000 | 20 | 15 | 0 | null | 0.75 | Datos insuficientes (AC=0), atrasado |

**Consolidado esperado**: BAC_total=44,000, CPI > 1, SPI ≈ 1 → proyecto en verde/amarillo.

**Edge case cubierto**: La actividad "Integración API externa" tiene AC=0 → CPI=null, razon_cpi="costo_real_es_cero".

---

## Proyecto 3: "Migración Base de Datos" (opcional, con 2 actividades mínimas para variedad)

**Narrativa**: Proyecto perfecto (CPI=1, SPI=1) — sirve para verificar el estado "en_presupuesto" / "en_cronograma".

| Actividad | BAC | % Plan | % Real | AC | CPI esperado | SPI esperado | Estado |
|-----------|-----|--------|--------|----|-------------|-------------|--------|
| Análisis de esquema | 5,000 | 50 | 50 | 2,500 | 1.0 | 1.0 | En presupuesto, en cronograma |
| Ejecución de migración | 10,000 | 30 | 30 | 3,000 | 1.0 | 1.0 | En presupuesto, en cronograma |
| Validación post-migración | 5,000 | 0 | 0 | 0 | null | null | Datos insuficientes ambos |

**Edge case cubierto**: Actividad con plan=0, real=0, AC=0 → todos los indicadores null.

---

## Resumen de cobertura de estados

| Estado | Representado por |
|--------|-----------------|
| `bajo_presupuesto` (CPI > 1) | Proyecto 2: Arquitectura, Inventario, Reportes |
| `en_presupuesto` (CPI = 1) | Proyecto 3: Análisis, Ejecución |
| `sobre_presupuesto` (CPI < 1) | Proyecto 1: todas las actividades |
| `datos_insuficientes` CPI | Proyecto 2: Integración (AC=0), Proyecto 3: Validación |
| `adelantado` (SPI > 1) | Proyecto 2: Inventario, Reportes |
| `en_cronograma` (SPI = 1) | Proyecto 2: Arquitectura, Proyecto 3: Análisis/Ejecución |
| `atrasado` (SPI < 1) | Proyecto 1: Frontend, Backend, QA |
| `datos_insuficientes` SPI | Proyecto 3: Validación (PV=0) |

---

## Notas de implementación

- Los UUIDs en el seed deben ser fijos (hardcodeados) para que sean reproducibles y referenciables en documentación
- El script debe ser idempotente: ejecutar `DELETE FROM activities; DELETE FROM projects;` antes de insertar (o usar `INSERT ... ON CONFLICT DO NOTHING` si se prefiere)
- El orden de inserción importa: primero projects, luego activities (por la FK)
- Todos los valores monetarios deben usar 2 decimales: `15000.00`, no `15000`
