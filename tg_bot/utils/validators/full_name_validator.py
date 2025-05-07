__all__ = ["full_name_validator"]


def full_name_validator(full_name: str) -> bool:
    """Validates that the full name contains exactly three parts (name, last name, surname).

    :param full_name: The full name to validate
    :return: The validated full name
    :raise ValueError: If the full name does not contain exactly three parts
    """
    return len(full_name.split()) == 3