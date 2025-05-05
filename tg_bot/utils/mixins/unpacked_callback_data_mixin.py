__all__ = ["UnpackedCallbackDataMixin"]
from typing import Generic, TypeVar

from aiogram.filters.callback_data import CallbackData


T = TypeVar('T', bound=CallbackData)

class UnpackedCallbackDataMixin(Generic[T]):
    callback_data: str

    def _get_t_class(self) -> type[T]:
        return self.__orig_bases__[0].__args__[0]

    @property
    def unpacked_callback_data(self) -> T:
        print(self._get_t_class())
        return self._get_t_class().unpack(self.callback_data)