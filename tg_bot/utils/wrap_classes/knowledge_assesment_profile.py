from __future__ import annotations
__all__ = ["KnowledgeAssesmentProfile"]
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tg_bot.models import KnowledgeAssesment, TestResult

class KnowledgeAssesmentProfile:
    def __init__(self, knowledge_assesment: KnowledgeAssesment, test_result: TestResult):
        self.knowledge_assesment = knowledge_assesment
        self.test_result = test_result