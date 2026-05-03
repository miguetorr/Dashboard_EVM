# AI_PROCESS.md — Registro de prompts de la sesión de exploración

Este archivo documenta todos los prompts enviados durante la sesión de exploración y diseño del proyecto **EVM Tracker V1**, previa a la implementación.

---

## Prompt 1 — Inicio de exploración

> tengo esto que te comparti en este archivo los requerimientos basicos que debe tener, necesito antes de empezar tener un plan estructurado, esquemas, modelado de la DB, necesito revisar todo lo documental primero para estar seguro de todo, sigue buenas practicas, quiero que todo funcione bajo contratos para asi evitar dependencias o bloqueantes

---

## Prompt 2 — Aclaración sobre el archivo de requerimientos

> se llama Primeros requerimientos no son los requerimientos que quiero que pongas en open spec pero si que tengas este contexto, si sugieres algo en algun punto sientete libre de decirmelo y lo revisamos

---

## Prompt 3 — Decisiones sobre el modelo y comportamiento del sistema

> si has la suma de componentes luego calcula
>
> Mejor en la fecha de corte que pusiste el cut_off_date en el modelo DB manejemoslo implicito que cuando la persona registe el porcentaje de avance a la fecha de corte esa fecha de corte es implicita en cuanto ingresa ese dato asi no tendriamos que hacer ningun tipo de calculo
>
> para los edge cases que pusiste la idea es que no crashee entonces  de esa forma que muestre null, pero que en el frontend no muestre null si no diga algo como que no se pude realiazar el calculo y mostrar el motivo o algo que visualmente sea bonito el null no se debe mostrar
>
> 1. por ahora en la V1 va a ser sin autenticacion entonces podemos dejar preparado eso para en caso de hacerlo no rompa nada ya que sera una v2 pero por ahora todos los lideres de proyecto ven lo de todos
>
> 2. lo respondi arriba pero basicamente manejemoslo implicito de cuando la persona registre ese avance
>
> 3. es mejor como lo piensas calculo en el cliente.
>
> 4. no este porcentaje no se puede superar en caso de que se supere muestre cmo una advertencia
>
> la migracion dejalo para v2 por ahora no

---

## Prompt 4 — Restricciones de la base de datos, idioma y UX

> en el esquema de la DB podemos poner en not null el bac, el planned_percentage, actual_percentage, actual_percentage
>
> adicional podemos añadir tambien en la DB las restricciones que no se hagan ni un insert ni un update si no cumple las siguientes reglas:
>
> bac tiene que ser positivo y actual_cost positivo tambien
> actual_percentage y planned_percentage solo admite de 0 a 100
>
> los Status los quiero en español y lo que ve el usuario en frontend tambien en español
>
> 1. modal/drawer
>
> 2. hard delete

---

## Prompt 5 — Confirmación de actual_cost, glosario, navegación y UX de actividades

> si tienes razon en esa parte me falto, manejalo como la opcion b >=
>
> me gustaria que en alguna parte diga como la explicacion de cada abreviatura para que sea clara la informacion asi sea personas que no manejan el tema.
>
> en caso de que se quiera cambiar de proyecto quiero que sea facil pasar de proyecto a proyecto. tambien que donde dice las actividades no salgan todas de una sino que tenga como un texto que diga ver mas o algo asi para dezplegar todas las actividades para no saturar la pantalla, tambien que cuando busquemos la forma mas bonita y facil de crear editar y eliminar los proyectos, tambien podemos agregar al lado del lapis de editar las actividades poner como una caneca que dice eliminar que si uno le rpesionea diga como desea elminar la actividad el nombre de la actividad y confimar si si o si no

---

## Prompt 6 — Solicitud de formalización en OpenSpec

> seria todo, ten encuenta todo el tema de pruebas unitarias y casos borde pero si ya podemos formalizar la propuesta

---

## Prompt 7 — Creacion de contrato OpenApi

> antes de continuar quisiera crear tambien el open api para que no halla ningun desfase despues o algun error.

---

## Prompt 8 — completar la documentacion

> que crees que podemos agregar a la documentacion para que nos ayude en la construccion final y tener todo claro 

---
## Prompt 9 — Implementacion de documentacion

> Si me parece completa lo sugerido

---

## Prompt 10 — Iniciar implementación del backend

> continua

*(Inicio de la sesión de implementación — sección 1: configuración del proyecto, estructura de directorios, requirements.txt, .flake8, pyproject.toml)*

---

## Prompt 11 — Continuar con base de datos

> continua

*(Sección 2: schema.sql con tablas projects y activities, constraints CHECK, cascade delete, seed.sql con datos de ejemplo, modelos SQLAlchemy, database.py)*

---

## Prompt 12 — Continuar con motor EVM

> continua

*(Sección 3: evm_constants.py, evm_calculator.py con calculate_activity_evm y calculate_project_evm, manejo de edge cases, redondeo con Decimal, 28 tests unitarios)*

---

## Prompt 13 — Continuar con schemas, repositorios y servicios

> continua

*(Secciones 4-6: schemas Pydantic, AbstractRepository, ProjectRepository, ActivityRepository, excepciones de dominio, ProjectService, ActivityService, AnonymousPrincipal para V2)*

---

## Prompt 14 — Continuar con routers y tests de integración

> continua

*(Secciones 7-8: routers de proyectos y actividades, main.py con CORS, conftest.py con SQLite en memoria, 38 tests de integración — total 66 tests, 98% cobertura)*

---

## Prompt 15 — Continuar con frontend tipos y utilidades

> continua

*(Sección 9: evm.ts con tipos TypeScript, evmCalculator.ts réplica del motor Python, client.ts con axios y 9 funciones tipadas)*

---

## Prompt 16 — Continuar con componentes compartidos

> continua

*(Sección 10: StatusBadge.tsx, ConfirmDialog.tsx, EVMGlossary.tsx con panel colapsable de definiciones en español)*

---

## Prompt 17 — Corrección en tasks.md

> la tarea 9.1 dice "git pullt:" en vez del nombre correcto y la sección 11 no está marcada aunque los archivos existen

---

## Prompt 18 — Continuar con página de lista de proyectos

> continua

*(Sección 11: ProjectCard.tsx, ProjectModal.tsx con patrón inner component + key, ProjectListPage.tsx con grid, estado vacío, modal de creación/edición, eliminación con ConfirmDialog)*

---

## Prompt 19 — Continuar con dashboard de proyecto

> continua

*(Sección 12: EVMIndicators.tsx con 10 indicadores y tooltips, ActivityTable.tsx con Ver más/menos, ActivityModal.tsx con preview EVM reactivo, EVMChart.tsx con Recharts, ProjectSelector.tsx breadcrumb, ProjectDashboardPage.tsx)*

---

## Prompt 20 — Continuar con routing y app

> continua

*(Sección 13: App.tsx con rutas /projects y /projects/:id, main.tsx con BrowserRouter + StrictMode, actualización de index.html, manejo de estados de carga y error)*

---

## Prompt 21 — Continuar con entregables finales

> continua

*(Sección 14: actualización README.md, verificación OpenAPI /docs, consistencia schemas, fix flake8 y ESLint — 4 errores react-hooks/set-state-in-effect resueltos con patrón inner component y reloadKey)*

---

## Prompt 22 — Continuar con la iteración (nueva sesión)

> Continuar: "¿Desea continuar con la iteración?"

---

## Prompt 23 — Verificar tareas pendientes reales

> en las tareas pendientes aun queda tareas sin realizar verificalas primero

---

## Prompt 24 — Solicitud de guía de configuración y pruebas

> necesito un archivo que indique como configurar y como poder probar el proyecto

---

## Prompt 25 — Pregunta sobre Node.js y simplificación del setup

> por que pide node.js si dijimos que esta python con fast api ?
>
> adicional hay alguna forma donde sea como ejecutar algo y haga automaticamente muchos procesos para no hacer tantos pasos para ejecutar siento que son muchos pasos y si alguien quiere hacer una prueba rapida no podria por que es bastante configuracion

---

## Prompt 26 — Coherencia entre guía rápida y guía detallada

> en el setup en la guia rapida dice que ejecute una configuracion que se llama setup ps1 y start ps1 pero en la guia detallada no aparece la ejecucion de estos archivos pienso que si ya con una tarea ya realizada para hacer estos ajustes rapido deberiamos usarla en la detallada

---

## Prompt 27 — Agregar prompts al AI_PROCESS.md

> en el archivo ai_process colocame todos los prompts de esta conversacion adicionando a los que ya estan

---

## Prompt 28 — Corrección de prompts faltantes

> faltan los iniciales me pusiste solo de la mitad para abajo

---

## Prompt 29 — Dejar AI_PROCESS como está

> dejalo asi

---

## Prompt 30 — README para entrega en GitHub

> ahora ayudame a esto me dicen esto
>
> Debe incluir un README.md con instrucciones para correr el proyecto localmente y el script de inicialización de la base de datos.
>
> es para entregar el github y que puedan hacerlo entonces no se si el setup sea muy largo para que se entrege en el github o como lo ves pero debo entregar esto

---

## Prompt 31 — Mejoras al README: credenciales, clonar repo, separar en SETUP

> en la guia rapida paso 2 no dice nada de colocar las credenciales entonces no se si colocarlas mejor, en el paso uno seria bueno como asegurate de estar en la carpeta de archivo, y antes de eso como clonar el repo algo asi
>
> para el readme no quede tan largo podemos dejar setup como pasos detallados y el readmi los rapidos y hacer referencia al final de si quieres un paso a paso detallado manualmente entra al archivo setup o no se si llamarlo diferente teniendo esto como objetivo, adicional en readme me gustaria poner toda la estructura del proyecto y pon los prompt nuevos los ultimos hablados en ia_process

---

## Prompt 32 — Error de Vite: falta style.css

> estaba haciendo pruebas y ejecute la tarea start.ps1 pero me sale este error
>
> [frontend] 5:11:49 p. m. [vite] Internal server error: Failed to resolve import "./style.css" from "src/main.tsx". Does the file exist?

---

## Prompt 33 — Error "No se pudieron cargar los proyectos" y problemas del frontend

> me sale este error
>
> EVM Tracker — No se pudieron cargar los proyectos. — Reintentar
>
> segun openspec teniamos unas pantallas para el front el texto sale mal sale con simbolos donde irian las tildes es muy plano y no se ve ninguna grafica entonces el fron tenemos que arreglarlo

---

## Prompt 34 — Correcciones múltiples: seed encoding, texto desbordado, diseño y explicaciones

> 1. toca ajustar seed para que tenga el tema de las tildes si toca ajustar hazlo y arregla el problema de raiz para que no ocurra
>
> 2. hay texto que se sale de sus casillas
>
> 3. me gustaria que fuera mas bonito y elegante
>
> 4. podrias explicarme cuando crea uno una actividad que es eso de porcentaje planificado y porcentaje real
>
> 5. cuando ingreso a http://localhost:8000 me manda directamente a docs

---

## Prompt 35 — Ajustar README y SETUP con las URLs correctas del backend

> entonces ajusta readme y setup que habla de dos localhost diferentes un 8000 y otro 8000/docs

---

## Prompt 36 — README paso 4 sigue con las dos URLs

> en el readme.md en el paso 4 sigue hablando de los dos como si fueran distintos

---

## Prompt 37 — Agregar últimos prompts a AI_PROCESS

> agrega los ultimos prompts a iaprocess

