"""Repositorio de proyectos."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.models import Project
from app.repositories.base import AbstractRepository


class ProjectRepository(AbstractRepository):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_all(self) -> list[Project]:
        return self.db.query(Project).order_by(Project.created_at.desc()).all()

    def get_by_id(self, project_id: UUID) -> Project | None:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def create(self, project: Project) -> Project:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, project: Project, data: dict) -> Project:
        for key, value in data.items():
            setattr(project, key, value)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()
