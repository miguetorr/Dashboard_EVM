"""Schemas Pydantic para indicadores EVM."""

from pydantic import BaseModel


class EVMResultSchema(BaseModel):
    """Indicadores EVM calculados para una actividad individual."""

    pv: float
    ev: float
    cv: float
    sv: float
    cpi: float | None
    spi: float | None
    eac: float | None
    vac: float | None
    estado_cpi: str
    estado_spi: str
    razon_cpi: str | None
    razon_spi: str | None

    model_config = {"from_attributes": True}


class EVMConsolidatedSchema(BaseModel):
    """Indicadores EVM consolidados para un proyecto (suma de componentes)."""

    bac_total: float
    pv: float
    ev: float
    ac: float
    cv: float
    sv: float
    cpi: float | None
    spi: float | None
    eac: float | None
    vac: float | None
    estado_cpi: str
    estado_spi: str
    razon_cpi: str | None
    razon_spi: str | None

    model_config = {"from_attributes": True}
