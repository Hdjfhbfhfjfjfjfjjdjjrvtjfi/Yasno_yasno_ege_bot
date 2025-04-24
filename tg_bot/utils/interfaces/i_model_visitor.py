__all__ = ["IModelVisitor"]
from abc import ABC, abstractmethod


class IModelVisitor(ABC):
    """Interface for visitor objects that operate on system models.
    
    This interface defines the contract for visitor objects in the
    visitor design pattern. Classes implementing this interface must
    provide visit methods for all types of objects they need to operate on.
    """
    
    @abstractmethod
    async def visit_administrator(self) -> None:
        """Visit and perform operations on an administrator object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_bot_user_profile(self) -> None:
        """Visit and perform operations on a bot user profile object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_excursion(self) -> None:
        """Visit and perform operations on an excursion object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_knowledge_assesment(self) -> None:
        """Visit and perform operations on a knowledge assessment object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_order(self) -> None:
        """Visit and perform operations on an order object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_school_grade(self) -> None:
        """Visit and perform operations on a school grade object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_test_answer(self) -> None:
        """Visit and perform operations on a test answer object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_test_question(self) -> None:
        """Visit and perform operations on a test question object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_test_response(self) -> None:
        """Visit and perform operations on a test response object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_test_result(self) -> None:
        """Visit and perform operations on a test result object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def visit_user(self) -> None:
        """Visit and perform operations on a user object.

        :return: None
        :raise NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError 