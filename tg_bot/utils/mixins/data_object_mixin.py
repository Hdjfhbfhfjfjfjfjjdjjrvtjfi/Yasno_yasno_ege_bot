__all__ = ["DataObjectMixin"]
from typing import Generic, TypeVar, Any


T = TypeVar("T")

class DataObjectMixin(Generic[T]):
    data: dict[str, Any]
    _data_object_argument_name: str

    @property
    def data_object(self) -> T:
        return self.data[self._data_object_argument_name]

    @data_object.setter
    def data_object(self, value: T) -> None:
        self.data[self._data_object_argument_name] = value