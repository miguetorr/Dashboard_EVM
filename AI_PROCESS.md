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
