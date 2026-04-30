"""Servicio de proyectos — orquesta repository + EVM calculator."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.evm_calculator import (
    EVMConsolidated,
    EVMResult,
    calculate_activity_evm,
    calculate_project_evm,
)
from app.core.principals import AnonymousPrincipal
from app.exceptions import ProjectNotFound
from app.models.models import Activity, Project
from app.repositories.activity_repository import ActivityRepository
from app.repositories.project_repository import ProjectRepository


class ProjectService:

    def __init__(self, db: Session, principal: AnonymousPrincipal | None = None) -> None:
        self.project_repo = ProjectRepository(db)
        self.activity_repo = ActivityRepository(db)
        self.principal = principal or AnonymousPrincipal()

    def list_projects(self) -> list[dict]:
        """Lista todos los proyectos con conteo de actividades y EVM consolidado."""
        projects = self.project_repo.get_all()
        result = []
        for project in projects:
            activities = project.activities
            evm = calculate_project_evm(activities)
            result.append({
                "project": project,
                "total_actividades": len(activities),
                "evm_consolidado": _evm_consolidated_to_dict(evm),
            })
        return result

    def get_project_detail(self, project_id: UUID) -> dict:
        """Retorna proyecto con actividades (cada una con EVM) y consolidado."""
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFound(str(project_id))

        activities = project.activities
        activities_with_evm = []
        for activity in activities:
            evm = calculate_activity_evm(
                activity.bac,
                activity.planned_percentage,
                activity.actual_percentage,
                activity.actual_cost,
            )
            activities_with_evm.append({
                "activity": activity,
                "evm": _evm_result_to_dict(evm),
            })

        evm_consolidated = calculate_project_evm(activities)

        return {
            "project": project,
            "actividades": activities_with_evm,
            "evm_consolidado": _evm_consolidated_to_dict(evm_consolidated),
        }

    def create(self, name: str, description: str | None = None) -> Project:
        project = Project(name=name, description=description)
        return self.project_repo.create(project)

    def update(self, project_id: UUID, data: dict) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFound(str(project_id))
        update_data = {k: v for k, v in data.items() if v is not None}
        if not update_data:
            return project
        return self.project_repo.update(project, update_data)

    def delete(self, project_id: UUID) -> None:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFound(str(project_id))
        self.project_repo.delete(project)


def _evm_result_to_dict(evm: EVMResult) -> dict:
    """Convierte EVMResult dataclass a dict serializable (Decimal → float)."""
    return {
        "pv": float(evm.pv),
        "ev": float(evm.ev),
        "cv": float(evm.cv),
        "sv": float(evm.sv),
        "cpi": float(evm.cpi) if evm.cpi is not None else None,
        "spi": float(evm.spi) if evm.spi is not None else None,
        "eac": float(evm.eac) if evm.eac is not None else None,
        "vac": float(evm.vac) if evm.vac is not None else None,
        "estado_cpi": evm.estado_cpi,
        "estado_spi": evm.estado_spi,
        "razon_cpi": evm.razon_cpi,
        "razon_spi": evm.razon_spi,
    }


def _evm_consolidated_to_dict(evm: EVMConsolidated) -> dict:
    """Convierte EVMConsolidated dataclass a dict serializable."""
    return {
        "bac_total": float(evm.bac_total),
        "pv": float(evm.pv),
        "ev": float(evm.ev),
        "ac": float(evm.ac),
        "cv": float(evm.cv),
        "sv": float(evm.sv),
        "cpi": float(evm.cpi) if evm.cpi is not None else None,
        "spi": float(evm.spi) if evm.spi is not None else None,
        "eac": float(evm.eac) if evm.eac is not None else None,
        "vac": float(evm.vac) if evm.vac is not None else None,
        "estado_cpi": evm.estado_cpi,
        "estado_spi": evm.estado_spi,
        "razon_cpi": evm.razon_cpi,
        "razon_spi": evm.razon_spi,
    }
