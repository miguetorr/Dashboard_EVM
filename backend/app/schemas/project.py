"""Schemas Pydantic para proyectos."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.activity import ActivityResponse
from app.schemas.evm import EVMConsolidatedSchema


class ProjectCreate(BaseModel):
    """Schema de creación de proyecto."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class ProjectUpdate(BaseModel):
    """Schema de edición de proyecto. Todos los campos opcionales."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None


class ProjectResponse(BaseModel):
    """Respuesta base de un proyecto (POST, PUT)."""

    id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    """Proyecto en la lista con resumen de actividades e indicadores consolidados."""

    id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    total_actividades: int
    evm_consolidado: EVMConsolidatedSchema

    model_config = {"from_attributes": True}


class ProjectDetailResponse(BaseModel):
    """Detalle de proyecto con actividades y EVM consolidado."""

    id: UUID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    actividades: list[ActivityResponse]
    evm_consolidado: EVMConsolidatedSchema

    model_config = {"from_attributes": True}
