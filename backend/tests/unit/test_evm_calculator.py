"""
Tests unitarios para el motor de cálculo EVM.

Cobertura:
  3.6  calculate_activity_evm — caso estándar, actividad completa, CPI/SPI=1
  3.7  Edge cases — AC=0, PV=0, actual_pct=0, todo en cero
  3.8  calculate_project_evm — consolidado, sin actividades, todas AC=0
  3.9  Interpretación de estados CPI/SPI en español
  3.10 Precisión de redondeo (índices a 4 dec, monetarios a 2 dec)
"""

from dataclasses import dataclass
from decimal import Decimal

import pytest

from app.core.evm_calculator import (
    EVMConsolidated,
    EVMResult,
    calculate_activity_evm,
    calculate_project_evm,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixture de actividad para tests de consolidación
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class MockActivity:
    bac: Decimal
    planned_percentage: Decimal
    actual_percentage: Decimal
    actual_cost: Decimal


# ═════════════════════════════════════════════════════════════════════════════
# 3.6 — calculate_activity_evm: casos estándar
# ═════════════════════════════════════════════════════════════════════════════


class TestCalculateActivityEvmEstandar:
    def test_caso_estandar_spec(self):
        """
        Escenario del spec: bac=10000, planned=60, actual=40, ac=7000
        PV=6000, EV=4000, CV=-3000, SV=-2000, CPI=0.5714, SPI=0.6667,
        EAC=17500, VAC=-7500
        """
        result = calculate_activity_evm(10000, 60, 40, 7000)

        assert result.pv == Decimal("6000.00")
        assert result.ev == Decimal("4000.00")
        assert result.cv == Decimal("-3000.00")
        assert result.sv == Decimal("-2000.00")
        assert result.cpi == Decimal("0.5714")
        assert result.spi == Decimal("0.6667")
        assert result.eac == Decimal("17500.00")
        assert result.vac == Decimal("-7500.00")

    def test_actividad_completa_en_presupuesto(self):
        """
        Escenario del spec: bac=5000, planned=100, actual=100, ac=5000
        PV=EV=5000, CV=SV=0, CPI=SPI=1.0, EAC=5000, VAC=0
        """
        result = calculate_activity_evm(5000, 100, 100, 5000)

        assert result.pv == Decimal("5000.00")
        assert result.ev == Decimal("5000.00")
        assert result.cv == Decimal("0.00")
        assert result.sv == Decimal("0.00")
        assert result.cpi == Decimal("1.0000")
        assert result.spi == Decimal("1.0000")
        assert result.eac == Decimal("5000.00")
        assert result.vac == Decimal("0.00")
        assert result.estado_cpi == "en_presupuesto"
        assert result.estado_spi == "en_cronograma"
        assert result.razon_cpi is None
        assert result.razon_spi is None

    def test_bajo_presupuesto_y_adelantado(self):
        """CPI > 1 y SPI > 1 — proyecto sano."""
        # EV = 10000*60/100 = 6000, PV = 10000*50/100 = 5000, AC = 4000
        # CPI = 6000/4000 = 1.5, SPI = 6000/5000 = 1.2
        result = calculate_activity_evm(10000, 50, 60, 4000)

        assert result.cpi == Decimal("1.5000")
        assert result.spi == Decimal("1.2000")
        assert result.estado_cpi == "bajo_presupuesto"
        assert result.estado_spi == "adelantado"


# ═════════════════════════════════════════════════════════════════════════════
# 3.7 — Edge cases
# ═════════════════════════════════════════════════════════════════════════════


class TestCalculateActivityEvmEdgeCases:
    def test_ac_cero_cpi_es_null(self):
        """AC=0 → CPI=null con razon_cpi, EAC=null, VAC=null."""
        result = calculate_activity_evm(10000, 60, 40, 0)

        assert result.cpi is None
        assert result.razon_cpi == "costo_real_es_cero"
        assert result.eac is None
        assert result.vac is None
        assert result.estado_cpi == "datos_insuficientes"

    def test_pv_cero_spi_es_null(self):
        """planned_percentage=0 → PV=0, SPI=null con razon_spi."""
        result = calculate_activity_evm(10000, 0, 0, 0)

        assert result.pv == Decimal("0.00")
        assert result.spi is None
        assert result.razon_spi == "valor_planificado_es_cero"
        assert result.estado_spi == "datos_insuficientes"

    def test_actual_pct_cero_con_costo_real(self):
        """
        actual_percentage=0, actual_cost=5000 → EV=0, CV=-5000,
        CPI=0 (calculable pero cero), EAC=null (sería infinito).
        """
        result = calculate_activity_evm(10000, 60, 0, 5000)

        assert result.ev == Decimal("0.00")
        assert result.cv == Decimal("-5000.00")
        assert result.cpi == Decimal("0.0000")
        assert result.razon_cpi is None  # CPI sí es calculable, vale 0
        assert result.eac is None  # BAC / 0 → no calculable
        assert result.vac is None
        assert result.estado_cpi == "sobre_presupuesto"

    def test_todo_en_cero(self):
        """
        planned=0, actual=0, ac=0 → todos los indicadores nulos o cero.
        Escenario "datos_insuficientes" en ambos índices.
        """
        result = calculate_activity_evm(10000, 0, 0, 0)

        assert result.pv == Decimal("0.00")
        assert result.ev == Decimal("0.00")
        assert result.cv == Decimal("0.00")
        assert result.sv == Decimal("0.00")
        assert result.cpi is None
        assert result.spi is None
        assert result.eac is None
        assert result.vac is None
        assert result.estado_cpi == "datos_insuficientes"
        assert result.estado_spi == "datos_insuficientes"
        assert result.razon_cpi == "costo_real_es_cero"
        assert result.razon_spi == "valor_planificado_es_cero"

    def test_actividad_sin_avance_planificado_spi_null(self):
        """planned_percentage=0 con AC real → SPI=null, CPI calculable."""
        result = calculate_activity_evm(8000, 0, 0, 2000)

        assert result.spi is None
        assert result.razon_spi == "valor_planificado_es_cero"
        # CPI = 0 / 2000 = 0 (calculable)
        assert result.cpi == Decimal("0.0000")
        assert result.razon_cpi is None


# ═════════════════════════════════════════════════════════════════════════════
# 3.8 — calculate_project_evm
# ═════════════════════════════════════════════════════════════════════════════


class TestCalculateProjectEvm:
    def test_consolidado_multiples_actividades(self):
        """
        Escenario del spec:
          A: bac=10000, planned=60, actual=40, ac=7000 → PV=6000, EV=4000, AC=7000
          B: bac=20000, planned=50, actual=30, ac=8000 → PV=10000, EV=6000, AC=8000
          Consolidado: PV=16000, EV=10000, AC=15000
          CPI = 10000/15000 = 0.6667
          SPI = 10000/16000 = 0.6250
        """
        activities = [
            MockActivity(Decimal("10000"), Decimal("60"), Decimal("40"), Decimal("7000")),
            MockActivity(Decimal("20000"), Decimal("50"), Decimal("30"), Decimal("8000")),
        ]
        result = calculate_project_evm(activities)

        assert result.bac_total == Decimal("30000.00")
        assert result.pv == Decimal("16000.00")
        assert result.ev == Decimal("10000.00")
        assert result.ac == Decimal("15000.00")
        assert result.cv == Decimal("-5000.00")
        assert result.sv == Decimal("-6000.00")
        assert result.cpi == Decimal("0.6667")
        assert result.spi == Decimal("0.6250")
        assert result.estado_cpi == "sobre_presupuesto"
        assert result.estado_spi == "atrasado"

    def test_sin_actividades(self):
        """Proyecto sin actividades → todo en 0 o null."""
        result = calculate_project_evm([])

        assert result.bac_total == Decimal("0")
        assert result.pv == Decimal("0")
        assert result.ev == Decimal("0")
        assert result.ac == Decimal("0")
        assert result.cpi is None
        assert result.spi is None
        assert result.eac is None
        assert result.vac is None
        assert result.estado_cpi == "datos_insuficientes"
        assert result.estado_spi == "datos_insuficientes"
        assert result.razon_cpi == "sin_actividades"
        assert result.razon_spi == "sin_actividades"

    def test_todas_actividades_ac_cero(self):
        """AC_total=0 → CPI_total=null con razon_cpi."""
        activities = [
            MockActivity(Decimal("5000"), Decimal("50"), Decimal("30"), Decimal("0")),
            MockActivity(Decimal("8000"), Decimal("70"), Decimal("50"), Decimal("0")),
        ]
        result = calculate_project_evm(activities)

        assert result.ac == Decimal("0.00")
        assert result.cpi is None
        assert result.razon_cpi == "costo_real_es_cero"
        assert result.estado_cpi == "datos_insuficientes"
        # SPI sí es calculable porque PV > 0
        assert result.spi is not None
        assert result.estado_spi != "datos_insuficientes"

    def test_consolidado_actividad_unica(self):
        """Consolidado con una sola actividad equivale al cálculo por actividad."""
        activity = MockActivity(Decimal("10000"), Decimal("60"), Decimal("40"), Decimal("7000"))
        result = calculate_project_evm([activity])

        assert result.bac_total == Decimal("10000.00")
        assert result.pv == Decimal("6000.00")
        assert result.ev == Decimal("4000.00")
        assert result.ac == Decimal("7000.00")
        assert result.cpi == Decimal("0.5714")
        assert result.spi == Decimal("0.6667")


# ═════════════════════════════════════════════════════════════════════════════
# 3.9 — Interpretación de estados CPI/SPI en español
# ═════════════════════════════════════════════════════════════════════════════


class TestInterpretacionEstados:
    # CPI states
    def test_cpi_mayor_uno_bajo_presupuesto(self):
        # EV=6000, AC=4000 → CPI=1.5 > 1
        result = calculate_activity_evm(10000, 50, 60, 4000)
        assert result.estado_cpi == "bajo_presupuesto"

    def test_cpi_igual_uno_en_presupuesto(self):
        # EV=5000, AC=5000 → CPI=1.0
        result = calculate_activity_evm(10000, 50, 50, 5000)
        assert result.estado_cpi == "en_presupuesto"

    def test_cpi_menor_uno_sobre_presupuesto(self):
        # EV=4000, AC=7000 → CPI=0.5714 < 1
        result = calculate_activity_evm(10000, 60, 40, 7000)
        assert result.estado_cpi == "sobre_presupuesto"

    def test_cpi_cero_sobre_presupuesto(self):
        # EV=0, AC=5000 → CPI=0 → sigue siendo sobre_presupuesto (0 < 1)
        result = calculate_activity_evm(10000, 60, 0, 5000)
        assert result.estado_cpi == "sobre_presupuesto"

    def test_cpi_null_datos_insuficientes(self):
        # AC=0 → CPI=null
        result = calculate_activity_evm(10000, 60, 40, 0)
        assert result.estado_cpi == "datos_insuficientes"

    # SPI states
    def test_spi_mayor_uno_adelantado(self):
        # EV=6000, PV=4000 → SPI=1.5 > 1
        result = calculate_activity_evm(10000, 40, 60, 5000)
        assert result.estado_spi == "adelantado"

    def test_spi_igual_uno_en_cronograma(self):
        # EV=5000, PV=5000 → SPI=1.0
        result = calculate_activity_evm(10000, 50, 50, 5000)
        assert result.estado_spi == "en_cronograma"

    def test_spi_menor_uno_atrasado(self):
        # EV=4000, PV=6000 → SPI=0.6667 < 1
        result = calculate_activity_evm(10000, 60, 40, 4000)
        assert result.estado_spi == "atrasado"

    def test_spi_null_datos_insuficientes(self):
        # PV=0 → SPI=null
        result = calculate_activity_evm(10000, 0, 0, 0)
        assert result.estado_spi == "datos_insuficientes"


# ═════════════════════════════════════════════════════════════════════════════
# 3.10 — Precisión de redondeo
# ═════════════════════════════════════════════════════════════════════════════


class TestPrecisionRedondeo:
    def test_cpi_redondeado_a_4_decimales(self):
        """EV=4000, AC=7000 → CPI = 4/7 = 0.571428... → 0.5714"""
        result = calculate_activity_evm(10000, 60, 40, 7000)
        assert result.cpi == Decimal("0.5714")

    def test_spi_redondeado_a_4_decimales(self):
        """EV=4000, PV=6000 → SPI = 2/3 = 0.666666... → 0.6667"""
        result = calculate_activity_evm(10000, 60, 40, 7000)
        assert result.spi == Decimal("0.6667")

    def test_cpi_redondeado_round_half_up(self):
        """Verifica que el redondeo es HALF_UP: 1/3=0.3333, 2/3=0.6667."""
        # CPI = 1/3: EV=1000, AC=3000
        result = calculate_activity_evm(10000, 100, 10, 3000)
        assert result.cpi == Decimal("0.3333")

    def test_eac_redondeado_a_2_decimales(self):
        """BAC=10000, CPI exacto=4/7 → EAC = 10000*(7/4) = 17500.00"""
        result = calculate_activity_evm(10000, 60, 40, 7000)
        assert result.eac == Decimal("17500.00")

    def test_pv_monetario_redondeado_a_2_decimales(self):
        """bac=10000, planned=33.33 → PV = 3333.00"""
        result = calculate_activity_evm(10000, "33.33", "0", 0)
        assert result.pv == Decimal("3333.00")

    def test_cv_monetario_redondeado_a_2_decimales(self):
        """EV=4000, AC=7000 → CV = -3000.00"""
        result = calculate_activity_evm(10000, 60, 40, 7000)
        assert result.cv == Decimal("-3000.00")

    def test_indices_consolidado_4_decimales(self):
        """CPI consolidado = 10000/15000 = 0.6667 (4 decimales)."""
        activities = [
            MockActivity(Decimal("10000"), Decimal("60"), Decimal("40"), Decimal("7000")),
            MockActivity(Decimal("20000"), Decimal("50"), Decimal("30"), Decimal("8000")),
        ]
        result = calculate_project_evm(activities)
        assert result.cpi == Decimal("0.6667")
        assert result.spi == Decimal("0.6250")
