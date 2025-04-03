__all__ = ["IVisitor"]
from abc import ABC, abstractmethod


class IVisitor(ABC):
    @abstractmethod
    async def visit_administrator(self) -> None:
        pass

    @abstractmethod
    async def visit_bot_user_profile(self) -> None:
        pass

    @abstractmethod
    async def visit_excursion(self) -> None:
        pass

    @abstractmethod
    async def visit_knowledge_assesment(self) -> None:
        pass

    @abstractmethod
    async def visit_order(self) -> None:
        pass

    @abstractmethod
    async def visit_school_grade(self) -> None:
        pass

    @abstractmethod
    async def visit_test_answer(self) -> None:
        pass

    @abstractmethod
    async def visit_test_question(self) -> None:
        pass

    @abstractmethod
    async def visit_test_response(self) -> None:
        pass

    @abstractmethod
    async def visit_test_result(self) -> None:
        pass

    @abstractmethod
    async def visit_user(self) -> None:
        pass
