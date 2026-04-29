
## Stack

- **Backend:** FastAPI (Python)
- **Base de datos:** PostgreSQL
- **Frontend:** React 

---

## El problema

>Queremos construir una herramienta interna para que los líderes de proyecto puedan registrar el avance de sus actividades y entender, en tiempo real, si su proyecto va bien o mal en términos de cronograma y presupuesto.
La metodología que usaremos para ese análisis es el Valor Ganado (Earned Value Management), un estándar del PMI que probablemente no conoces. Eso está bien — de hecho, es parte intencional del ejercicio. Tendrás que aprenderlo durante el desarrollo.
La idea central del Valor Ganado es sencilla: no basta con saber cuánto has gastado ni cuánto has avanzado por separado. Lo que importa es la relación entre los dos. Un proyecto puede haber gastado el 60% del presupuesto habiendo completado solo el 40% del trabajo — y eso es una señal de alerta. Los indicadores EVM te permiten cuantifi car exactamente eso.

## que se debe construir 

> Una aplicación fullstack que permita gestionar proyectos y sus actividades, y que calcule automáticamente los indicadores de Valor Ganado.

### Backend

> Necesitamos una API REST que exponga operaciones para crear, editar y eliminar proyectos y actividades. Cada actividad debe registrar los siguientes datos:
- Nombre
- Presupuesto total planifi cado (BAC — Budget at Completion)
- Porcentaje de avance planifi cado a la fecha de corte
- Porcentaje de avance real completado
- Costo real incurrido hasta la fecha (AC — Actual Cost)
Con esos datos, el sistema debe calcular automáticamente los siguientes indicadores por actividad y de forma consolidada por proyecto:

| Indicador | Fórmula |
|-----------|----------|
| PV (Planned Value)| `porcentaje_planificado × bac` |
| EV (Earned Value)| `porcentaje_real × bac` |
| CV (Cost Variance)| `EV − AC` |
| SV (Schedule Variance)| `EV − PV` |
| CPI (Cost Performance Index)| `EV / AC` |
| SPI (Schedule Performance Index)| `EV / PV` |
| EAC Estimate at Completion| `BAC / CPI` |
| VAC (Variance at Completion)| `BAC − EAC` |

El API también debe retornar la interpretación de CPI y SPI: si el proyecto está bajo presupuesto o sobre presupuesto, adelantado o atrasado. Un CPI mayor a 1 indica efi ciencia en costos; menor a 1 indica que se está gastando más de lo que se avanza. El SPI funciona con la misma lógica pero sobre el cronograma.




### Frontend — pantallas requeridas

### Dashboard del proyecto
Un dashboard donde el líder de proyecto pueda ingresar y editar sus actividades, y ver el resultado del análisis en tiempo real. Debe incluir la tabla de actividades con sus indicadores calculados, los indicadores consolidados del proyecto, una indicación visual del estado de CPI y SPI, y una gráfi ca que compare PV, EV y AC por actividad.
No pedimos un diseño elaborado. Pedimos que la información sea clara y que quien la mire entienda de un vistazo si el proyecto va bien o mal.

## Estándares de calidad

### Pruebas
- Cobertura mínima: **80% en lógica de negocio**
- Tests unitarios para la lógica de cálculo EVM
- Tests de integración por endpoint del API
- Casos borde: AC = 0, % real = 0, % real > 100

### Código limpio
- Separación clara: controladores no contienen lógica de negocio
- Nombres descriptivos (no abreviaciones crípticas)
- Sin código muerto ni comentarios innecesarios
-Cero code smells. El código debe estar limpio. Sin bloques comentados, sin variables sin usar, sin números o strings mágicos dispersos por el código. Los nombres de variables, métodos y clases deben ser descriptivos. La lógica de negocio no debe vivir en los controladores. Si una función hace más de una cosa, probablemente deba dividirse. Si un bloque de lógica se repite más de dos veces, debe abstraerse. Recomendamos confi gurar un linter en el proyecto — si lo haces, incluye la confi guración en el repositorio.
Gitfl ow estricto. El historial de tu repositorio es parte de la entrega. La estructura
-OpenAPI/Swagger. Valoramos positivamente que el API esté documentado con la especifi cación OpenAPI. Si lo implementas, debe ser accesible localmente en /api-docs o /swagger-ui, y cada endpoint debe incluir descripción, esquemas de request y response, y los posibles códigos de error. Hacerlo bien demuestra que entiendes el contrato del API como un artefacto de comunicación, no solo como documentación.

## Entregable técnico

- `README.md` del proyecto: instrucciones para levantar backend, frontend y BD
- Script SQL: DDL con tablas + datos de ejemplo (seed)
