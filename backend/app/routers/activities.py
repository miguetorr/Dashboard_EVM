"""Router de actividades — capa HTTP, solo enrutamiento."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import ActivityNotFound, ProjectNotFound
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.activity_service import ActivityService

router = APIRouter(
    prefix="/api/v1/projects/{project_id}/activities",
    tags=["Actividades"],
)


def _get_service(db: Session = Depends(get_db)) -> ActivityService:
    return ActivityService(db)


@router.get("", response_model=list[ActivityResponse])
def list_activities(
    project_id: UUID,
    service: ActivityService = Depends(_get_service),
):
    """Listar actividades de un proyecto con EVM calculado."""
    try:
        items = service.list_by_project(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    return [
        {
            "id": item["activity"].id,
            "project_id": item["activity"].project_id,
            "name": item["activity"].name,
            "bac": float(item["activity"].bac),
            "planned_percentage": float(item["activity"].planned_percentage),
            "actual_percentage": float(item["activity"].actual_percentage),
            "actual_cost": float(item["activity"].actual_cost),
            "created_at": item["activity"].created_at,
            "updated_at": item["activity"].updated_at,
            "evm": item["evm"],
        }
        for item in items
    ]


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    project_id: UUID,
    body: ActivityCreate,
    service: ActivityService = Depends(_get_service),
):
    """Crear una nueva actividad en un proyecto."""
    try:
        result = service.create(
            project_id=project_id,
            name=body.name,
            bac=body.bac,
            planned_percentage=body.planned_percentage,
            actual_percentage=body.actual_percentage,
            actual_cost=body.actual_cost,
        )
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    return {
        "id": result["activity"].id,
        "project_id": result["activity"].project_id,
        "name": result["activity"].name,
        "bac": float(result["activity"].bac),
        "planned_percentage": float(result["activity"].planned_percentage),
        "actual_percentage": float(result["activity"].actual_percentage),
        "actual_cost": float(result["activity"].actual_cost),
        "created_at": result["activity"].created_at,
        "updated_at": result["activity"].updated_at,
        "evm": result["evm"],
    }


@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity(
    project_id: UUID,
    activity_id: UUID,
    body: ActivityUpdate,
    service: ActivityService = Depends(_get_service),
):
    """Editar una actividad (EVM se recalcula automáticamente)."""
    try:
        result = service.update(activity_id, body.model_dump(exclude_unset=True))
    except ActivityNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada",
        )

    return {
        "id": result["activity"].id,
        "project_id": result["activity"].project_id,
        "name": result["activity"].name,
        "bac": float(result["activity"].bac),
        "planned_percentage": float(result["activity"].planned_percentage),
        "actual_percentage": float(result["activity"].actual_percentage),
        "actual_cost": float(result["activity"].actual_cost),
        "created_at": result["activity"].created_at,
        "updated_at": result["activity"].updated_at,
        "evm": result["evm"],
    }


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    project_id: UUID,
    activity_id: UUID,
    service: ActivityService = Depends(_get_service),
):
    """Eliminar una actividad."""
    try:
        service.delete(activity_id)
    except ActivityNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Actividad no encontrada",
        )
