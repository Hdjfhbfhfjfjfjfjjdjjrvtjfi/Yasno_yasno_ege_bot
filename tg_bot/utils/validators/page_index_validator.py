__all__ = ["page_index_validator"]


def page_index_validator(index: int, max_index: int) -> int:
    if index < 0:
        index = max_index
    if index > max_index:
        index = 0
    return  index