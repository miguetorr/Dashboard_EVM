"""Excepciones de dominio."""


class ProjectNotFound(Exception):
    """El proyecto solicitado no existe."""

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id
        super().__init__(f"Proyecto no encontrado: {project_id}")


class ActivityNotFound(Exception):
    """La actividad solicitada no existe."""

    def __init__(self, activity_id: str) -> None:
        self.activity_id = activity_id
        super().__init__(f"Actividad no encontrada: {activity_id}")
