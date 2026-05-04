"""
Motor de cálculo EVM (Earned Value Management).

Módulo de funciones puras — sin estado, sin I/O, sin dependencias externas.
Acepta cualquier tipo numérico (int, float, Decimal) y trabaja internamente
con Decimal para garantizar precisión financiera.

Convenciones de redondeo:
- Índices (CPI, SPI):              4 decimales  (ROUND_HALF_UP)
- Valores monetarios (PV, EV, ...): 2 decimales  (ROUND_HALF_UP)
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from app.core.evm_constants import (
    ADELANTADO,
    ATRASADO,
    BAJO_PRESUPUESTO,
    DATOS_INSUFICIENTES,
    EN_CRONOGRAMA,
    EN_PRESUPUESTO,
    RAZON_COSTO_REAL_ES_CERO,
    RAZON_SIN_ACTIVIDADES,
    RAZON_VALOR_PLANIFICADO_ES_CERO,
    SOBRE_PRESUPUESTO,
)

# ─────────────────────────────────────────────────────────────────────────────
# Constantes Decimal
# ─────────────────────────────────────────────────────────────────────────────
_ZERO = Decimal("0")
_ONE = Decimal("1")
_HUNDRED = Decimal("100")
_MONETARY_PLACES = Decimal("0.01")
_INDEX_PLACES = Decimal("0.0001")


# ─────────────────────────────────────────────────────────────────────────────
# Data classes de resultado (inmutables)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class EVMResult:
    """Indicadores EVM calculados para una actividad individual."""

    pv: Decimal
    ev: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    estado_cpi: str
    estado_spi: str
    razon_cpi: str | None
    razon_spi: str | None


@dataclass(frozen=True)
class EVMConsolidated:
    """Indicadores EVM consolidados para un proyecto (suma de componentes)."""

    bac_total: Decimal
    pv: Decimal
    ev: Decimal
    ac: Decimal
    cv: Decimal
    sv: Decimal
    cpi: Decimal | None
    spi: Decimal | None
    eac: Decimal | None
    vac: Decimal | None
    estado_cpi: str
    estado_spi: str
    razon_cpi: str | None
    razon_spi: str | None


# ─────────────────────────────────────────────────────────────────────────────
# Helpers privados
# ─────────────────────────────────────────────────────────────────────────────


def _to_decimal(value: Any) -> Decimal:
    """Convierte cualquier numérico a Decimal de forma segura."""
    return Decimal(str(value))


def _round_monetary(value: Decimal) -> Decimal:
    return value.quantize(_MONETARY_PLACES, rounding=ROUND_HALF_UP)


def _round_index(value: Decimal) -> Decimal:
    return value.quantize(_INDEX_PLACES, rounding=ROUND_HALF_UP)


def _interpret_cpi(cpi: Decimal | None) -> str:
    if cpi is None:
        return DATOS_INSUFICIENTES
    if cpi > _ONE:
        return BAJO_PRESUPUESTO
    if cpi == _ONE:
        return EN_PRESUPUESTO
    return SOBRE_PRESUPUESTO  # cpi < 1 (incluyendo 0)


def _interpret_spi(spi: Decimal | None) -> str:
    if spi is None:
        return DATOS_INSUFICIENTES
    if spi > _ONE:
        return ADELANTADO
    if spi == _ONE:
        return EN_CRONOGRAMA
    return ATRASADO  # spi < 1 (incluyendo 0)


def _compute_eac_vac(
    bac: Decimal, cpi: Decimal | None
) -> tuple[Decimal | None, Decimal | None]:
    """
    Calcula EAC = BAC / CPI y VAC = BAC - EAC.
    Retorna (None, None) cuando CPI es nulo o cero (resultado sería infinito).
    El cálculo usa el CPI exacto (sin redondear) para evitar errores acumulados.
    """
    if cpi is None or cpi == _ZERO:
        return None, None
    eac = bac / cpi
    vac = bac - eac
    return eac, vac


# ─────────────────────────────────────────────────────────────────────────────
# API pública
# ─────────────────────────────────────────────────────────────────────────────


def calculate_activity_evm(
    bac: Any,
    planned_pct: Any,
    actual_pct: Any,
    actual_cost: Any,
) -> EVMResult:
    """
    Calcula los 8 indicadores EVM para una actividad.

    Args:
        bac:          Presupuesto hasta la conclusión
                      (Budget at Completion). Debe ser > 0.
        planned_pct:  Porcentaje de avance planificado (0-100).
        actual_pct:   Porcentaje de avance real (0-100).
        actual_cost:  Costo real incurrido. Debe ser >= 0.

    Returns:
        EVMResult con todos los indicadores, estados e interpretaciones en español.
        Los campos cpi, spi, eac y vac pueden ser None con su razón correspondiente.
    """
    bac_d = _to_decimal(bac)
    planned_d = _to_decimal(planned_pct)
    actual_d = _to_decimal(actual_pct)
    ac = _to_decimal(actual_cost)

    # Valores base
    pv = bac_d * planned_d / _HUNDRED
    ev = bac_d * actual_d / _HUNDRED
    cv = ev - ac
    sv = ev - pv

    # CPI = EV / AC  (null si AC = 0 — no hay costo real registrado)
    cpi: Decimal | None
    razon_cpi: str | None
    if ac == _ZERO:
        cpi = None
        razon_cpi = RAZON_COSTO_REAL_ES_CERO
    else:
        cpi = ev / ac
        razon_cpi = None

    # SPI = EV / PV  (null si PV = 0 — nada estaba planificado aún)
    spi: Decimal | None
    razon_spi: str | None
    if pv == _ZERO:
        spi = None
        razon_spi = RAZON_VALOR_PLANIFICADO_ES_CERO
    else:
        spi = ev / pv
        razon_spi = None

    # EAC = BAC / CPI  (null si CPI es null o cero → sería infinito)
    eac, vac = _compute_eac_vac(bac_d, cpi)

    return EVMResult(
        pv=_round_monetary(pv),
        ev=_round_monetary(ev),
        cv=_round_monetary(cv),
        sv=_round_monetary(sv),
        cpi=_round_index(cpi) if cpi is not None else None,
        spi=_round_index(spi) if spi is not None else None,
        eac=_round_monetary(eac) if eac is not None else None,
        vac=_round_monetary(vac) if vac is not None else None,
        # Interpretación desde valores exactos (antes del redondeo)
        estado_cpi=_interpret_cpi(cpi),
        estado_spi=_interpret_spi(spi),
        razon_cpi=razon_cpi,
        razon_spi=razon_spi,
    )


def calculate_project_evm(activities: list) -> EVMConsolidated:
    """
    Calcula los indicadores EVM consolidados de un proyecto usando suma de componentes
    (estándar PMI): se suman PV, EV y AC de todas las actividades y luego se
    calculan los índices sobre esas sumas.

    Args:
        activities: Lista de objetos con atributos bac, planned_percentage,
                    actual_percentage y actual_cost (e.g. modelos ORM Activity).

    Returns:
        EVMConsolidated. Si la lista está vacía, todos los valores son 0 o None.
    """
    if not activities:
        return EVMConsolidated(
            bac_total=_ZERO,
            pv=_ZERO,
            ev=_ZERO,
            ac=_ZERO,
            cv=_ZERO,
            sv=_ZERO,
            cpi=None,
            spi=None,
            eac=None,
            vac=None,
            estado_cpi=DATOS_INSUFICIENTES,
            estado_spi=DATOS_INSUFICIENTES,
            razon_cpi=RAZON_SIN_ACTIVIDADES,
            razon_spi=RAZON_SIN_ACTIVIDADES,
        )

    bac_total = _ZERO
    total_pv = _ZERO
    total_ev = _ZERO
    total_ac = _ZERO

    for activity in activities:
        bac_d = _to_decimal(activity.bac)
        planned_d = _to_decimal(activity.planned_percentage)
        actual_d = _to_decimal(activity.actual_percentage)
        ac_d = _to_decimal(activity.actual_cost)

        bac_total += bac_d
        total_pv += bac_d * planned_d / _HUNDRED
        total_ev += bac_d * actual_d / _HUNDRED
        total_ac += ac_d

    cv = total_ev - total_ac
    sv = total_ev - total_pv

    # CPI consolidado
    cpi: Decimal | None
    razon_cpi: str | None
    if total_ac == _ZERO:
        cpi = None
        razon_cpi = RAZON_COSTO_REAL_ES_CERO
    else:
        cpi = total_ev / total_ac
        razon_cpi = None

    # SPI consolidado
    spi: Decimal | None
    razon_spi: str | None
    if total_pv == _ZERO:
        spi = None
        razon_spi = RAZON_VALOR_PLANIFICADO_ES_CERO
    else:
        spi = total_ev / total_pv
        razon_spi = None

    # EAC y VAC consolidados
    eac, vac = _compute_eac_vac(bac_total, cpi)

    return EVMConsolidated(
        bac_total=_round_monetary(bac_total),
        pv=_round_monetary(total_pv),
        ev=_round_monetary(total_ev),
        ac=_round_monetary(total_ac),
        cv=_round_monetary(cv),
        sv=_round_monetary(sv),
        cpi=_round_index(cpi) if cpi is not None else None,
        spi=_round_index(spi) if spi is not None else None,
        eac=_round_monetary(eac) if eac is not None else None,
        vac=_round_monetary(vac) if vac is not None else None,
        estado_cpi=_interpret_cpi(cpi),
        estado_spi=_interpret_spi(spi),
        razon_cpi=razon_cpi,
        razon_spi=razon_spi,
    )
