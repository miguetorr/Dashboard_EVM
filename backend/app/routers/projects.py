"""Router de proyectos — capa HTTP, solo enrutamiento."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import ProjectNotFound
from app.schemas.project import (
    ProjectCreate,
    ProjectDetailResponse,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/api/v1/projects", tags=["Proyectos"])


def _get_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


@router.get("", response_model=list[ProjectListResponse])
def list_projects(service: ProjectService = Depends(_get_service)):
    """Listar todos los proyectos con resumen EVM consolidado."""
    items = service.list_projects()
    return [
        {
            "id": item["project"].id,
            "name": item["project"].name,
            "description": item["project"].description,
            "created_at": item["project"].created_at,
            "updated_at": item["project"].updated_at,
            "total_actividades": item["total_actividades"],
            "evm_consolidado": item["evm_consolidado"],
        }
        for item in items
    ]


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    body: ProjectCreate,
    service: ProjectService = Depends(_get_service),
):
    """Crear un nuevo proyecto."""
    return service.create(name=body.name, description=body.description)


@router.get("/{project_id}", response_model=ProjectDetailResponse)
def get_project_detail(
    project_id: UUID,
    service: ProjectService = Depends(_get_service),
):
    """Obtener detalle de un proyecto con actividades y EVM."""
    try:
        detail = service.get_project_detail(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    return {
        "id": detail["project"].id,
        "name": detail["project"].name,
        "description": detail["project"].description,
        "created_at": detail["project"].created_at,
        "updated_at": detail["project"].updated_at,
        "actividades": [
            {
                "id": a["activity"].id,
                "project_id": a["activity"].project_id,
                "name": a["activity"].name,
                "bac": float(a["activity"].bac),
                "planned_percentage": float(a["activity"].planned_percentage),
                "actual_percentage": float(a["activity"].actual_percentage),
                "actual_cost": float(a["activity"].actual_cost),
                "created_at": a["activity"].created_at,
                "updated_at": a["activity"].updated_at,
                "evm": a["evm"],
            }
            for a in detail["actividades"]
        ],
        "evm_consolidado": detail["evm_consolidado"],
    }


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    body: ProjectUpdate,
    service: ProjectService = Depends(_get_service),
):
    """Editar nombre y/o descripción de un proyecto."""
    try:
        return service.update(project_id, body.model_dump(exclude_unset=True))
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(_get_service),
):
    """Eliminar un proyecto y todas sus actividades (cascade)."""
    try:
        service.delete(project_id)
    except ProjectNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )
