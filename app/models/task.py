from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional
from ..db import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped["Goal"] = relationship(back_populates="tasks")
    
    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = False if not self.completed_at else True

        if self.goal:
            task_as_dict["goal_id"] = self.goal.id

        return task_as_dict
    
    @classmethod
    def from_dict(cls, dict_data):
        return cls(title=dict_data["title"], description=dict_data["description"])