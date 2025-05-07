from __future__ import annotations
__all__ = ["SchoolGrade"]
from tortoise import Model
from tortoise.fields import IntField, ManyToManyField

from typing import TYPE_CHECKING, Optional

from tg_bot.utils.interfaces import ICanAcceptModelVisitors
from tg_bot.utils.metaclasses import CombinedModelAndABCMeta
if TYPE_CHECKING:
    from tg_bot.utils.data_objects import SchoolGradeData
    from tg_bot.utils.interfaces import IModelVisitor


class SchoolGrade(Model, ICanAcceptModelVisitors, metaclass=CombinedModelAndABCMeta):
    """Model representing a school grade in the system.
    
    :ivar grade: Integer primary key field representing the grade level
    :ivar questions: Many-to-many relationship with TestQuestion model
    """
    grade = IntField(pk=True)
    questions = ManyToManyField("models.TestQuestion")

    @classmethod
    async def accept(cls, visitor: IModelVisitor) -> None:
        """Accepts a model visitor and triggers the school grade visit method.
        
        :param visitor: The model visitor implementing IModelVisitor interface
        :return: None
        """
        await visitor.visit_school_grade()

    @classmethod
    async def get_by_id(cls, grade_id: int) -> Optional["SchoolGrade"]:
        """Retrieves a school grade by its ID.
        
        :param grade_id: The grade id to retrieve
        :return: The SchoolGrade instance if found, None otherwise
        """
        return await cls.get_or_none(grade=grade_id)

    @classmethod
    async def get_grades_tuple(cls) -> tuple[int, ...]:
        """Retrieves all available grades as a tuple.
        
        :return: Tuple containing all grades
        """
        return tuple(await cls.all().values_list("grade", flat=True))

    @classmethod
    async def create_school_grade(cls, school_grade_data: SchoolGradeData) -> "SchoolGrade":
        """Creates a new school grade from the provided data.
        
        :param school_grade_data: SchoolGradeData object containing the grade details
        :return: The newly created SchoolGrade instance
        """
        school_grade = SchoolGrade(grade=school_grade_data.grade)
        await school_grade.save()
        return school_grade