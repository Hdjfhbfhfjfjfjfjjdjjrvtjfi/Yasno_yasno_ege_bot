from __future__ import annotations
__all__ = ["KnowledgeAssesmentProfile"]
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tg_bot.models import KnowledgeAssesment, TestResult


class KnowledgeAssesmentProfile:
    """
    A wrapper class that combines a knowledge assessment with its associated test result.
    
    This class serves as a container for related knowledge assessment and test result data,
    making it easier to work with these related entities as a single unit.

    :cvar knowledge_assesment: The wrapped knowledge assessment object
    :cvar test_result: The wrapped test result object
    """

    def __init__(self, knowledge_assesment: KnowledgeAssesment, test_result: TestResult) -> None:
        """
        Initializes a new KnowledgeAssesmentProfile instance.
        
        :param knowledge_assesment: The knowledge assessment object
        :param test_result: The associated test result object
        :return: None
        """
        self.knowledge_assesment: KnowledgeAssesment = knowledge_assesment
        self.test_result: TestResult = test_result