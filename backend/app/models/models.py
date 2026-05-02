import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    activities = relationship(
        "Activity",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Project {self.name}>"


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("bac > 0", name="chk_bac_positive"),
        CheckConstraint("actual_cost >= 0", name="chk_actual_cost_non_negative"),
        CheckConstraint(
            "planned_percentage >= 0 AND planned_percentage <= 100",
            name="chk_planned_percentage_range",
        ),
        CheckConstraint(
            "actual_percentage >= 0 AND actual_percentage <= 100",
            name="chk_actual_percentage_range",
        ),
        Index("idx_activities_project_id", "project_id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    bac = Column(Numeric(14, 2), nullable=False)
    planned_percentage = Column(Numeric(5, 2), nullable=False, default=0)
    actual_percentage = Column(Numeric(5, 2), nullable=False, default=0)
    actual_cost = Column(Numeric(14, 2), nullable=False, default=0)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    project = relationship("Project", back_populates="activities")

    def __repr__(self) -> str:
        return f"<Activity {self.name}>"
