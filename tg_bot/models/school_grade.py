from __future__ import annotations
__all__ = ["SchoolGrade"]
from tortoise import Model
from tortoise.fields import IntField, ManyToManyField

from typing import TYPE_CHECKING, Optional

from tg_bot.utils.interfaces import ICanAcceptVisitor
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.data_objects import SchoolGradeData
    from tg_bot.utils.interfaces import IVisitor


class SchoolGrade(Model, ICanAcceptVisitor, metaclass=CombinedModelAndABCMeta):
    grade = IntField(pk=True)
    questions = ManyToManyField("models.TestQuestion")

    @classmethod
    async def accept(cls, visitor: IVisitor) -> None:
        await visitor.visit_school_grade()

    @classmethod
    async def get_by_id(cls, grade_id: int) -> Optional["SchoolGrade"]:
        return await cls.get_or_none(grade=grade_id)

    @classmethod
    async def get_grades_tuple(cls) -> tuple[int, ...]:
        return tuple(await cls.all().values_list("grade", flat=True))

    @classmethod
    async def create_school_grade(cls, school_grade_data: SchoolGradeData) -> "SchoolGrade":
        school_grade = SchoolGrade(grade=school_grade_data.grade)
        await school_grade.save()
        return school_grade