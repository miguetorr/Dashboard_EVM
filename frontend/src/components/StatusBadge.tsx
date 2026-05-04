import type { EVMCpiStatus, EVMSpiStatus } from "../types/evm";

type EVMStatus = EVMCpiStatus | EVMSpiStatus;

interface StatusBadgeProps {
  status: EVMStatus;
  value?: number | null;
  reason?: string | null;
}

const STATUS_CONFIG: Record<EVMStatus, { label: string; className: string }> = {
  bajo_presupuesto: { label: "Bajo presupuesto", className: "badge--success" },
  en_presupuesto: { label: "En presupuesto", className: "badge--neutral" },
  sobre_presupuesto: { label: "Sobre presupuesto", className: "badge--danger" },
  adelantado: { label: "Adelantado", className: "badge--success" },
  en_cronograma: { label: "En cronograma", className: "badge--neutral" },
  atrasado: { label: "Atrasado", className: "badge--danger" },
  datos_insuficientes: { label: "Sin datos", className: "badge--disabled" },
};

const REASON_LABELS: Record<string, string> = {
  costo_real_es_cero: "El costo real es cero",
  valor_planificado_es_cero: "El valor planificado es cero",
  sin_actividades: "Sin actividades",
};

export default function StatusBadge({ status, value, reason }: StatusBadgeProps) {
  const config = STATUS_CONFIG[status];

  const displayValue =
    value !== null && value !== undefined ? value.toFixed(4) : "N/A";

  const tooltip = reason ? REASON_LABELS[reason] ?? reason : undefined;

  return (
    <span
      className={`badge ${config.className}`}
      title={tooltip}
    >
      {displayValue} — {config.label}
    </span>
  );
}
