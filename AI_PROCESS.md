# Herramientas de IA utilizadas

> las herrmaientas de ira que use fueron 3:

* chatGpt: es la que mas he usado y me gusta como explica las coas entonces muchas de las dudad que me generan las resuelvo con esta IA

* Claude: me gusta usarla cuando necesito poner en contexto de algun proyecto que tengo, me aydua a aclarar dudas tecnicas y a generar un preliminar de una primera documentacion

* Copilot + Openspec: basicamente openspec la uso para plasmar toda mi idea desde el punto inicia hasta los ultimos test, me ayduaa estrusturar la idea que tengo y de como quiero hacer las cosas, y luego de eso a implementarlas de forma eficiente siguiendo un plan

# Cómo aprendí EVM

> Primero estuve investigando por mi cuenta y le pregunté a Claude cuando apenas estaba empezando el proyecto. Me dio una explicación, pero la verdad no me quedó muy clara. Después le pregunté a ChatGPT, pero esta vez planteándole directamente qué era lo que quería hacer, y ahí sí me lo explicó mucho más sencillo.

Básicamente entendí que todo se resume en responder tres preguntas clave. Ya cuando empecé a hacer la documentación con OpenSpec, todo terminó de hacer clic y lo entendí mucho mejor.

---

# Reflexión sobre qué haría diferente si repitiera el ejercicio

> Si tuviera que repetir el ejercicio, le pondría mucho más cuidado al frontend. El diseño que terminé implementando no quedó del todo como me lo imaginaba desde el inicio. Siento que en la fase de documentación me enfoqué más en cómo iba a funcionar todo y en lo que debía devolver, y dejé un poco de lado la parte visual.

Al final, eso se nota: la aplicación cumple, pero le falta ese toque para que sea más atractiva y agradable de ver. Creo que debería haber definido mejor desde el principio cómo quería que se viera, no solo cómo debía funcionar, para que el resultado final quedara más completo.

---

# Decisiones en las que no seguí a la IA

## Decisión 1: Usar Python + FastAPI en lugar de Node.js + Express

**Contexto:**
Al inicio del proyecto, consulté con Claude sobre qué stack usar. Mencioné que manejo Python pero no soy experto. Claude me sugirió Node.js + Express argumentando que sería más rápido y seria el mismo lenguaje que React en el frontend (JavaScript/TypeScript).

**Mi decisión:**
Decidí usar Python + FastAPI de todas formas, por las siguientes razones:

1. **Precisión financiera:** Python tiene el tipo `Decimal` nativo en la biblioteca estándar, mientras que JavaScript requiere librerías externas (`decimal.js`) para manejar aritmética financiera sin errores de redondeo.

2. **Validación declarativa:** Pydantic (que FastAPI usa internamente) valida los schemas de datos de forma declarativa, reduciendo código boilerplate en comparación con validadores de Express.

3. **Testing robusto:** Pytest con fixtures y tests parametrizados es más maduro.

5. **Familiaridad suficiente:** Aunque no soy experto en Python, el documento dice "usa el stack con el que tengas mayor dominio" — y mi conocimiento de Python es suficiente para este proyecto.

**Cómo validé la decisión:**
Antes de iniciar con la implementacion, investigué la documentación de FastAPI y confirmé que podía cumplir todos los requisitos (OpenAPI, tests unitarios, separación en capas) en el tiempo disponible.

**Resultado:**
La implementación final tiene 66 tests con 98% de cobertura, documentación OpenAPI completa en `/docs`, y el motor de cálculo EVM usa `Decimal` garantizando precisión exacta en todos los cálculos financieros.

---


# Decisiones de arquitectura

---

## Decisión 1: Edición mediante modal

**Contexto:**
El frontend necesita permitir editar actividades con 5 campos: nombre, BAC, porcentaje planificado, porcentaje real, y costo real. Evalué dos opciones:

1. **Inline editing:** Hacer clic en una celda de la tabla la convierte en campo editable
2. **Modal/Drawer:** Botón "Editar" que abre un formulario completo

**Mi decisión:**
Usar un modal con formulario completo.

**Razonamiento:**
1. **Claridad sobre velocidad:** El documento dice explícitamente "No pedimos un diseño elaborado. Pedimos que la información sea clara"
2. **Complejidad vs tiempo:** Inline editing bien hecho (manejo de focus, validaciones en celda, estado por campo) puede tomar mas tiempo
3. **Múltiples campos:** Con 5 campos editables por actividad, inline editing se vuelve confuso
4. **Validaciones claras:** En un modal puedo mostrar mensajes de error junto a cada campo; en inline es más difícil

**Cómo cumple "tiempo real":**
El requerimiento de análisis "en tiempo real" lo cumplí con **cálculo en el cliente dentro del modal**: mientras el usuario edita los campos, React recalcula los indicadores EVM instantáneamente sin llamar al API. Al guardar, se persiste en backend.

---

## Decisión 2: Fecha de corte implícita en lugar de campo explícito

**Contexto:**
El documento de requirements especifica que cada actividad debe registrar "porcentaje de avance planificado a la fecha de corte", pero no define Fecha de corte como un campo del sistema.

En EVM tradicional, la fecha de corte es un snapshot formal del proyecto en un momento específico. Inicialmente consideré agregar un campo fecha de corte como editable en el modelo de datos.

**Mi decisión:**
No agregar fecha de corte como campo en la base de datos. La fecha de corte es implícita: cuando el líder de proyecto ingresa el porcentaje de avance planificado, ese valor ya captura la intención para "el momento actual".

**Razonamiento:**
1. **El documento no lo pide:** El requerimiento pide el "porcentaje planificado a la fecha de corte", no la fecha misma
2. **Simplicidad del modelo:** El usuario ya hizo el cálculo mental ("hoy deberíamos estar al 60%")
3. **Sin cálculos adicionales:** No necesitamos lógica para calcular porcentajes basados en fechas y cronogramas

---

# ChatGPT

---

## Prompt 1 — Explicación EVM

> explicame que es EVM estoy en un proyecto donde tengo que sacar unos indicadores este es el problema Queremos construir una herramienta interna para que los líderes de proyecto puedan registrar el avance de sus actividades y entender, en tiempo real, si su proyecto va bien o mal en términos de cronograma y presupuesto. La metodología que usaremos para ese análisis es el Valor Ganado (Earned Value Management), un estándar del PMI que probablemente no conoces. Eso está bien — de hecho, es parte intencional del ejercicio. Tendrás que aprenderlo durante el desarrollo. La idea central del Valor Ganado es sencilla: no basta con saber cuánto has gastado ni cuánto has avanzado por separado. Lo que importa es la relación entre los dos. Un proyecto puede haber gastado el 60% del presupuesto habiendo completado solo el 40% del trabajo — y eso es una señal de alerta. Los indicadores EVM te permiten cuantifi car exactamente eso

---

## Prompt 2 — Estructura del PR

> ayudame a colocar bien la descripcion de un pr ya hice toda la documentacin de un proyecto que incluye todo desde el back el la base de datos, todo lo documental para open spec y el open api lo quiero en formato md para que se vea mas bonito

---

# Claude

---

## Prompt 1 — Inicio de exploración

> necesito hacer que me ayudes a hacer un plan sobre este problema que tengo, quiero que se incluyan todos los criterios que te coloque y que resuelva el problema descrito, ademas necesito entender todo super bien

---

## Prompt 2 — Elección de stack tecnológico

P: ¿Con qué stack tecnológico te sientes más cómodo?
R: quiero una comparacion entre las dos opciones y que me digas cual recomiendas y por que seria mejor para este caso

P: ¿Qué tan familiarizado estás con EVM (Earned Value Management)?
R: No lo conozco para nada asi que necesito entenderlo muy bien antes

P: ¿Qué necesitas primero?
R: Ambos juntos

---

## Prompt 3 — Solicitud de plan estructurado

por ahora lo del evm dejemoslo para despues por ahora centremosnos en lo otro 

yo manejo y me siento mas como con pero si dices que es mejor node js por velocidad me parece bien

---

## Prompt 4 — Solicitud de explicación de EVM

me puedes explicar como se halla el EVM no lo entendi muy bien explicamelo un poco mas detallado

---

## Prompt 5 — Pregunta sobre BAC

tengo una duda el bac el bac se definiria por proyecto y se mantendria a lo largo del proyecto o bac es la suma del presupuesto de cada actividad y cada actividad tiene su propio bac

---

# Copilot + OpenSpec

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

## Prompt 7 — Creación de contrato OpenAPI

> antes de continuar quisiera crear tambien el open api para que no halla ningun desfase despues o error que se presente en el futuro

---

## Prompt 8 — Empezar con la implementación

> empecemos con lo primero la configuracion del proyecto y quiero que todo lo hagas con open spec usa opsx-apply no se si quieres lo hago directamente que es mejor ?

---

## Prompt 9 — Crear el .gitignore y corregir errores del GitHub

> antes de seguir creame un git ignore de todo lo que no se debe subir al repo y arregla si hay algun error

---

## Prompt 10 — Arreglo de errores del GitHub

> Ayudame a arreglar el main se habian subido los archivos que estaban en git ignore 

---

## Prompt 11 — Arreglo main gitignore

> no quiero que se mergee develop ya que quiero mantener el git flow lo mas que se pueda entonces arreglemoslo sin tocar develop y manteniendo el git flow lo mas limpio posible

---

## Prompt 12 — Creación rama fix

> si creemos una rama fix para solucionar este problema y sincroniza todo con github despues subiendo eso que hicimos sincroniza todo con local y el github para tener todo limpio y poder seguir

---

## Prompt 13 — Sección 2

> Perfecto podemos continuar con la seccion numero 2, utiliza openspec para hacerlo segun lo definido previamente utilizando sus skills

---

## Prompt 14 — Sección 3

> Si sigamos con la siguiente seccion y ya no hagas nada en git a menos que te lo indique por ahora lo are manual yo

---

## Prompt 15 — Sección 4

> Si sigue con la seccion 4, ten encuenta todo lo de openspec y adicional actualiza el tasks ya se completo de la seccion 1 a la 3

---

## Prompt 16 — Verificación tareas 4

> no veo creado el ProjectDetailResponse pero lo marcaste como realizado

---

## Prompt 17 — Sección 5

> Perfecto continuemos con la seccion 5 recuerda tener presente las skills de open spec

---

## Prompt 18 — Sección 6–12 (no se pide nada diferente, solo que se continúe con la implementación)

> si continual con la siguiente seccion

---

## Prompt 19 — Corrección en tasks.md

> la sección 11 no está marcada aunque los archivos existen

---

## Prompt 20 — Sección 13–14

> continua con la seccion 13 y tambien con la 14 y asegurate de hacer todos los test

---

## Prompt 21 — Solicitud de guía de configuración y pruebas

> necesito que crees un archivo que indique como configurar y como poder probar el proyecto

---

## Prompt 22 — Simplificación del setup

> quiero que los pasos para ejecutar la configuracion no sea tan larga con tantos pasos entonces quiero que crees un tarea que haga automaticamente muchos procesos para no hacer tantos pasos para ejecutar siento que son muchos pasos y si alguien quiere hacer una prueba rapida no podria por que es bastante configuracion

---

## Prompt 23 — Coherencia entre guía rápida y guía detallada

> en el setup en la guia rapida dice que ejecute una configuracion que se llama setup ps1 y start ps1 pero en la guia detallada no aparece la ejecucion de estos archivos pienso que si ya con una tarea ya realizada para hacer estos ajustes rapido deberiamos usarla en la detallada

---

## Prompt 24 — README para entrega en GitHub

> ahora ayudame a esto
>
> quiero que el README.md quede con instrucciones para correr el proyecto localmente y el script de inicialización de la base de datos.
>
> es para que se pueda ver en el github y que puedan hacerlo entonces no se si de alguna forma ponemos la configuracion en este readme para que se vea en github

---

## Prompt 25 — Mejoras al README: credenciales, clonar repo, separar en SETUP

> en la guia rapida paso 2 no dice nada de colocar las credenciales entonces no se si colocarlas mejor, en el paso uno seria bueno como asegurate de estar en la carpeta de archivo, y antes de eso como clonar el repo algo asi
>
> para el readme no quede tan largo podemos dejar setup como pasos detallados y el readmi los rapidos y hacer referencia al final de si quieres un paso a paso detallado manualmente entra al archivo setup o no se si llamarlo diferente teniendo esto como objetivo, adicional en readme me gustaria poner toda la estructura del proyecto

---

## Prompt 26 — Error de Vite: falta style.css

> estaba haciendo pruebas y ejecute la tarea start.ps1 pero me encontre este error entonces creo que falto crearlo
>
> [frontend] 5:11:49 p. m. [vite] Internal server error: Failed to resolve import "./style.css" from "src/main.tsx". Does the file exist?

---

## Prompt 27 — Error "No se pudieron cargar los proyectos" y problemas del frontend

> me sale este error
>
> EVM Tracker — No se pudieron cargar los proyectos. — Reintentar
>
> segun openspec teniamos unas pantallas para el front el texto sale mal sale con simbolos donde irian las tildes es muy plano y no se ve ninguna grafica entonces el front tenemos que arreglarlo.

---

## Prompt 28 — Correcciones múltiples: seed encoding, texto desbordado, diseño y explicaciones

> 1. toca ajustar seed para que tenga el tema de las tildes si toca ajustar hazlo y arregla el problema de raiz para que no ocurra
>
> 2. hay texto que se sale de sus casillas entonces ponlo con ... si no se alcanza a mostrar todo
>
> 3. me gustaria que fuera mas bonito y elegante siento que es muy plano el css
>
> 4. el http://localhost:8000 me manda directamente a docs entonces en este sentido tenemos algo diferente que hace lo mismo

---

## Prompt 29 — Ajustar README y SETUP con las URLs correctas del backend

> entonces ajusta readme y setup que habla de dos localhost diferentes un 8000 y otro 8000/docs

---

## Prompt 30 — README paso 4 sigue con las dos URLs

> en el readme.md en el paso 4 sigue hablando de los dos como si fueran distintos

---