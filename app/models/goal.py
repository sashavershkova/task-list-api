from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .task import Task


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")
    
    def to_dict(self, include_empty_tasks=False):
        goal_as_dict = {}
        goal_as_dict["id"] = self.id
        goal_as_dict["title"] = self.title

        if self.tasks:
            goal_as_dict["tasks"] = [task.to_dict() for task in self.tasks]
        if not self.tasks and include_empty_tasks == True:
            goal_as_dict["tasks"] = []

        return goal_as_dict
    
    # def to_dict_mandatory_tasks_list(self):
    #     goal_as_dict = self.to_dict()
    #     goal_as_dict["tasks"] = [task.to_dict() for task in self.tasks]
    #     return goal_as_dict
    

    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])