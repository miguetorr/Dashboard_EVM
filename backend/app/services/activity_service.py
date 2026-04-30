"""Servicio de actividades — orquesta repository + validación de proyecto."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.evm_calculator import EVMResult, calculate_activity_evm
from app.core.principals import AnonymousPrincipal
from app.exceptions import ActivityNotFound, ProjectNotFound
from app.models.models import Activity
from app.repositories.activity_repository import ActivityRepository
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import _evm_result_to_dict


class ActivityService:

    def __init__(self, db: Session, principal: AnonymousPrincipal | None = None) -> None:
        self.activity_repo = ActivityRepository(db)
        self.project_repo = ProjectRepository(db)
        self.principal = principal or AnonymousPrincipal()

    def list_by_project(self, project_id: UUID) -> list[dict]:
        """Lista actividades de un proyecto con EVM calculado por cada una."""
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFound(str(project_id))

        activities = self.activity_repo.get_by_project_id(project_id)
        result = []
        for activity in activities:
            evm = calculate_activity_evm(
                activity.bac,
                activity.planned_percentage,
                activity.actual_percentage,
                activity.actual_cost,
            )
            result.append({
                "activity": activity,
                "evm": _evm_result_to_dict(evm),
            })
        return result

    def create(
        self, project_id: UUID, name: str, bac: float,
        planned_percentage: float, actual_percentage: float, actual_cost: float,
    ) -> dict:
        """Crea una actividad validando que el proyecto exista."""
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFound(str(project_id))

        activity = Activity(
            project_id=project_id,
            name=name,
            bac=bac,
            planned_percentage=planned_percentage,
            actual_percentage=actual_percentage,
            actual_cost=actual_cost,
        )
        created = self.activity_repo.create(activity)
        evm = calculate_activity_evm(
            created.bac,
            created.planned_percentage,
            created.actual_percentage,
            created.actual_cost,
        )
        return {"activity": created, "evm": _evm_result_to_dict(evm)}

    def update(self, activity_id: UUID, data: dict) -> dict:
        """Actualiza una actividad y recalcula EVM."""
        activity = self.activity_repo.get_by_id(activity_id)
        if not activity:
            raise ActivityNotFound(str(activity_id))

        update_data = {k: v for k, v in data.items() if v is not None}
        if update_data:
            activity = self.activity_repo.update(activity, update_data)

        evm = calculate_activity_evm(
            activity.bac,
            activity.planned_percentage,
            activity.actual_percentage,
            activity.actual_cost,
        )
        return {"activity": activity, "evm": _evm_result_to_dict(evm)}

    def delete(self, activity_id: UUID) -> None:
        activity = self.activity_repo.get_by_id(activity_id)
        if not activity:
            raise ActivityNotFound(str(activity_id))
        self.activity_repo.delete(activity)
