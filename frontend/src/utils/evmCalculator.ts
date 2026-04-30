/**
 * Motor de cálculo EVM (Earned Value Management) — versión TypeScript.
 *
 * Réplica exacta de la lógica del backend Python para cálculo reactivo local
 * en el frontend (ej. vista previa en el modal de actividad).
 *
 * Convenciones de redondeo:
 * - Índices (CPI, SPI):              4 decimales
 * - Valores monetarios (PV, EV, ...): 2 decimales
 */

import type { EVMResult, EVMConsolidated, EVMCpiStatus, EVMSpiStatus } from "../types/evm";
import {
  CPI_STATUS,
  SPI_STATUS,
  DATOS_INSUFICIENTES,
  EVM_REASONS,
} from "../types/evm";

// ─────────────────────────────────────────────────────────────────────────────
// Helpers privados
// ─────────────────────────────────────────────────────────────────────────────

function roundMonetary(value: number): number {
  return Math.round(value * 100) / 100;
}

function roundIndex(value: number): number {
  return Math.round(value * 10000) / 10000;
}

function interpretCpi(cpi: number | null): EVMCpiStatus {
  if (cpi === null) return DATOS_INSUFICIENTES;
  if (cpi > 1) return CPI_STATUS.BAJO_PRESUPUESTO;
  if (cpi === 1) return CPI_STATUS.EN_PRESUPUESTO;
  return CPI_STATUS.SOBRE_PRESUPUESTO;
}

function interpretSpi(spi: number | null): EVMSpiStatus {
  if (spi === null) return DATOS_INSUFICIENTES;
  if (spi > 1) return SPI_STATUS.ADELANTADO;
  if (spi === 1) return SPI_STATUS.EN_CRONOGRAMA;
  return SPI_STATUS.ATRASADO;
}

// ─────────────────────────────────────────────────────────────────────────────
// API pública
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Calcula los indicadores EVM para una actividad individual.
 *
 * @param bac          Presupuesto hasta la conclusión (> 0)
 * @param plannedPct   Porcentaje de avance planificado (0-100)
 * @param actualPct    Porcentaje de avance real (0-100)
 * @param actualCost   Costo real incurrido (>= 0)
 */
export function calculateActivityEvm(
  bac: number,
  plannedPct: number,
  actualPct: number,
  actualCost: number,
): EVMResult {
  const pv = (bac * plannedPct) / 100;
  const ev = (bac * actualPct) / 100;
  const cv = ev - actualCost;
  const sv = ev - pv;

  // CPI = EV / AC  (null si AC = 0)
  let cpi: number | null;
  let razon_cpi: string | null;
  if (actualCost === 0) {
    cpi = null;
    razon_cpi = EVM_REASONS.COSTO_REAL_ES_CERO;
  } else {
    cpi = ev / actualCost;
    razon_cpi = null;
  }

  // SPI = EV / PV  (null si PV = 0)
  let spi: number | null;
  let razon_spi: string | null;
  if (pv === 0) {
    spi = null;
    razon_spi = EVM_REASONS.VALOR_PLANIFICADO_ES_CERO;
  } else {
    spi = ev / pv;
    razon_spi = null;
  }

  // EAC = BAC / CPI  (null si CPI es null o 0)
  let eac: number | null;
  let vac: number | null;
  if (cpi === null || cpi === 0) {
    eac = null;
    vac = null;
  } else {
    eac = bac / cpi;
    vac = bac - eac;
  }

  return {
    pv: roundMonetary(pv),
    ev: roundMonetary(ev),
    cv: roundMonetary(cv),
    sv: roundMonetary(sv),
    cpi: cpi !== null ? roundIndex(cpi) : null,
    spi: spi !== null ? roundIndex(spi) : null,
    eac: eac !== null ? roundMonetary(eac) : null,
    vac: vac !== null ? roundMonetary(vac) : null,
    estado_cpi: interpretCpi(cpi),
    estado_spi: interpretSpi(spi),
    razon_cpi,
    razon_spi,
  };
}

/**
 * Datos mínimos de una actividad para el cálculo consolidado.
 */
interface ActivityData {
  bac: number;
  planned_percentage: number;
  actual_percentage: number;
  actual_cost: number;
}

/**
 * Calcula los indicadores EVM consolidados de un proyecto usando
 * suma de componentes (estándar PMI).
 */
export function calculateProjectEvm(activities: ActivityData[]): EVMConsolidated {
  if (activities.length === 0) {
    return {
      bac_total: 0,
      pv: 0,
      ev: 0,
      ac: 0,
      cv: 0,
      sv: 0,
      cpi: null,
      spi: null,
      eac: null,
      vac: null,
      estado_cpi: DATOS_INSUFICIENTES,
      estado_spi: DATOS_INSUFICIENTES,
      razon_cpi: EVM_REASONS.SIN_ACTIVIDADES,
      razon_spi: EVM_REASONS.SIN_ACTIVIDADES,
    };
  }

  let bacTotal = 0;
  let totalPv = 0;
  let totalEv = 0;
  let totalAc = 0;

  for (const a of activities) {
    bacTotal += a.bac;
    totalPv += (a.bac * a.planned_percentage) / 100;
    totalEv += (a.bac * a.actual_percentage) / 100;
    totalAc += a.actual_cost;
  }

  const cv = totalEv - totalAc;
  const sv = totalEv - totalPv;

  // CPI consolidado
  let cpi: number | null;
  let razon_cpi: string | null;
  if (totalAc === 0) {
    cpi = null;
    razon_cpi = EVM_REASONS.COSTO_REAL_ES_CERO;
  } else {
    cpi = totalEv / totalAc;
    razon_cpi = null;
  }

  // SPI consolidado
  let spi: number | null;
  let razon_spi: string | null;
  if (totalPv === 0) {
    spi = null;
    razon_spi = EVM_REASONS.VALOR_PLANIFICADO_ES_CERO;
  } else {
    spi = totalEv / totalPv;
    razon_spi = null;
  }

  // EAC y VAC consolidados
  let eac: number | null;
  let vac: number | null;
  if (cpi === null || cpi === 0) {
    eac = null;
    vac = null;
  } else {
    eac = bacTotal / cpi;
    vac = bacTotal - eac;
  }

  return {
    bac_total: roundMonetary(bacTotal),
    pv: roundMonetary(totalPv),
    ev: roundMonetary(totalEv),
    ac: roundMonetary(totalAc),
    cv: roundMonetary(cv),
    sv: roundMonetary(sv),
    cpi: cpi !== null ? roundIndex(cpi) : null,
    spi: spi !== null ? roundIndex(spi) : null,
    eac: eac !== null ? roundMonetary(eac) : null,
    vac: vac !== null ? roundMonetary(vac) : null,
    estado_cpi: interpretCpi(cpi),
    estado_spi: interpretSpi(spi),
    razon_cpi,
    razon_spi,
  };
}
