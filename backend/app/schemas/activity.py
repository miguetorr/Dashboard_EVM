"""Schemas Pydantic para actividades."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.evm import EVMResultSchema


class ActivityCreate(BaseModel):
    """Schema de creación de actividad."""

    name: str = Field(..., min_length=1, max_length=255)
    bac: float = Field(..., gt=0)
    planned_percentage: float = Field(..., ge=0, le=100)
    actual_percentage: float = Field(..., ge=0, le=100)
    actual_cost: float = Field(..., ge=0)


class ActivityUpdate(BaseModel):
    """Schema de edición de actividad. Todos los campos opcionales."""

    name: str | None = Field(None, min_length=1, max_length=255)
    bac: float | None = Field(None, gt=0)
    planned_percentage: float | None = Field(None, ge=0, le=100)
    actual_percentage: float | None = Field(None, ge=0, le=100)
    actual_cost: float | None = Field(None, ge=0)


class ActivityResponse(BaseModel):
    """Respuesta de actividad con indicadores EVM calculados."""

    id: UUID
    project_id: UUID
    name: str
    bac: float
    planned_percentage: float
    actual_percentage: float
    actual_cost: float
    created_at: datetime
    updated_at: datetime
    evm: EVMResultSchema

    model_config = {"from_attributes": True}
