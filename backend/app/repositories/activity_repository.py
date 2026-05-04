"""Repositorio de actividades."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.models import Activity
from app.repositories.base import AbstractRepository


class ActivityRepository(AbstractRepository):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_by_project_id(self, project_id: UUID) -> list[Activity]:
        return (
            self.db.query(Activity)
            .filter(Activity.project_id == project_id)
            .order_by(Activity.created_at.asc())
            .all()
        )

    def get_all(self) -> list[Activity]:
        return self.db.query(Activity).order_by(Activity.created_at.asc()).all()

    def get_by_id(self, activity_id: UUID) -> Activity | None:
        return self.db.query(Activity).filter(Activity.id == activity_id).first()

    def create(self, activity: Activity) -> Activity:
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def update(self, activity: Activity, data: dict) -> Activity:
        for key, value in data.items():
            setattr(activity, key, value)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def delete(self, activity: Activity) -> None:
        self.db.delete(activity)
        self.db.commit()
