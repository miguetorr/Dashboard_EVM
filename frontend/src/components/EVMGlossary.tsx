import { useState } from "react";

const GLOSSARY_ITEMS = [
  {
    term: "BAC",
    formula: "Suma de presupuestos",
    description:
      "Budget at Completion — Presupuesto total del proyecto. Es la suma del BAC de cada actividad.",
  },
  {
    term: "PV",
    formula: "BAC × % Planificado / 100",
    description:
      "Planned Value — Valor planificado. Cuánto trabajo debería estar hecho según el plan.",
  },
  {
    term: "EV",
    formula: "BAC × % Real / 100",
    description:
      "Earned Value — Valor ganado. Cuánto trabajo realmente se ha completado, valorado al presupuesto.",
  },
  {
    term: "AC",
    formula: "Costo real registrado",
    description:
      "Actual Cost — Costo real. Cuánto dinero se ha gastado realmente hasta ahora.",
  },
  {
    term: "CV",
    formula: "EV − AC",
    description:
      "Cost Variance — Variación de costo. Positivo = ahorrando dinero. Negativo = gastando de más.",
  },
  {
    term: "SV",
    formula: "EV − PV",
    description:
      "Schedule Variance — Variación de cronograma. Positivo = adelantado. Negativo = atrasado.",
  },
  {
    term: "CPI",
    formula: "EV / AC",
    description:
      "Cost Performance Index — Índice de rendimiento de costo. Mayor a 1 = eficiente. Menor a 1 = ineficiente.",
  },
  {
    term: "SPI",
    formula: "EV / PV",
    description:
      "Schedule Performance Index — Índice de rendimiento de cronograma. Mayor a 1 = adelantado. Menor a 1 = atrasado.",
  },
  {
    term: "EAC",
    formula: "BAC / CPI",
    description:
      "Estimate at Completion — Estimación al finalizar. Cuánto se espera que cueste el proyecto si el rendimiento actual se mantiene.",
  },
  {
    term: "VAC",
    formula: "BAC − EAC",
    description:
      "Variance at Completion — Variación al finalizar. Positivo = terminará bajo presupuesto. Negativo = terminará sobre presupuesto.",
  },
];

export default function EVMGlossary() {
  const [open, setOpen] = useState(false);

  return (
    <div className="glossary">
      <button
        type="button"
        className="glossary__toggle"
        onClick={() => setOpen(!open)}
      >
        {open ? "▾" : "▸"} ¿Qué significan estos indicadores?
      </button>

      {open && (
        <dl className="glossary__list">
          {GLOSSARY_ITEMS.map((item) => (
            <div key={item.term} className="glossary__item">
              <dt className="glossary__term">
                {item.term}{" "}
                <code className="glossary__formula">{item.formula}</code>
              </dt>
              <dd className="glossary__description">{item.description}</dd>
            </div>
          ))}
        </dl>
      )}
    </div>
  );
}
