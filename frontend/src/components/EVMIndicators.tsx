import type { EVMConsolidated } from "../types/evm";
import StatusBadge from "./StatusBadge";

interface IndicatorDef {
  key: keyof EVMConsolidated;
  label: string;
  formula: string;
  description: string;
  isIndex?: boolean;
}

const INDICATORS: IndicatorDef[] = [
  { key: "bac_total", label: "BAC", formula: "Suma de presupuestos", description: "Presupuesto total del proyecto." },
  { key: "pv", label: "PV", formula: "BAC × % Planificado / 100", description: "Valor planificado según el plan." },
  { key: "ev", label: "EV", formula: "BAC × % Real / 100", description: "Valor del trabajo realmente completado." },
  { key: "ac", label: "AC", formula: "Costo real registrado", description: "Costo real incurrido hasta ahora." },
  { key: "cv", label: "CV", formula: "EV − AC", description: "Positivo = ahorrando. Negativo = gastando de más." },
  { key: "sv", label: "SV", formula: "EV − PV", description: "Positivo = adelantado. Negativo = atrasado." },
  { key: "cpi", label: "CPI", formula: "EV / AC", description: "Índice de rendimiento de costo. Mayor a 1 = eficiente.", isIndex: true },
  { key: "spi", label: "SPI", formula: "EV / PV", description: "Índice de rendimiento de cronograma. Mayor a 1 = adelantado.", isIndex: true },
  { key: "eac", label: "EAC", formula: "BAC / CPI", description: "Estimación de costo final si el rendimiento se mantiene." },
  { key: "vac", label: "VAC", formula: "BAC − EAC", description: "Positivo = bajo presupuesto. Negativo = sobre presupuesto." },
];

interface EVMIndicatorsProps {
  data: EVMConsolidated;
}

export default function EVMIndicators({ data }: EVMIndicatorsProps) {
  return (
    <div className="indicators">
      {INDICATORS.map((ind) => {
        const raw = data[ind.key];
        const value = typeof raw === "number" ? raw : null;

        // CPI y SPI tienen badges de estado
        if (ind.key === "cpi") {
          return (
            <div
              key={ind.key}
              className="indicator"
              title={`${ind.label} = ${ind.formula} — ${ind.description}`}
            >
              <span className="indicator__label">{ind.label}</span>
              <StatusBadge
                status={data.estado_cpi}
                value={data.cpi}
                reason={data.razon_cpi}
              />
            </div>
          );
        }

        if (ind.key === "spi") {
          return (
            <div
              key={ind.key}
              className="indicator"
              title={`${ind.label} = ${ind.formula} — ${ind.description}`}
            >
              <span className="indicator__label">{ind.label}</span>
              <StatusBadge
                status={data.estado_spi}
                value={data.spi}
                reason={data.razon_spi}
              />
            </div>
          );
        }

        // Indicadores monetarios y otros
        const displayValue =
          value !== null
            ? ind.isIndex
              ? value.toFixed(4)
              : `$${value.toLocaleString("es-CO", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
            : "N/A";

        return (
          <div
            key={ind.key}
            className="indicator"
            title={`${ind.label} = ${ind.formula} — ${ind.description}`}
          >
            <span className="indicator__label">{ind.label}</span>
            <span className="indicator__value">{displayValue}</span>
          </div>
        );
      })}
    </div>
  );
}
