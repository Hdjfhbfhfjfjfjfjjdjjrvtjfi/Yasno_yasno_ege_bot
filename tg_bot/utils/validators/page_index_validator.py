__all__ = ["page_index_validator"]


def page_index_validator(index: int, max_index: int) -> int:
    """Validates and normalizes a page index to ensure it stays within valid bounds.

    This function implements circular navigation for page indices:
    - If the index is negative, it wraps around to the maximum index
    - If the index exceeds the maximum, it wraps around to 0

    :param index: The current page index to validate
    :param max_index: The maximum valid page index
    :return: The normalized page index that is guaranteed to be within valid bounds
    """
    if index < 0:
        index = max_index
    if index > max_index:
        index = 0
    return index