__all__ = ["phone_number_validator"]
from phonenumbers import parse, NumberParseException


def phone_number_validator(phone_number: str) -> bool:
    """Validates that the phone number is in a valid format.

    :param phone_number: The phone number to validate
    :return: The normalized phone number in international format
    :raise ValueError: If the phone number is not in a valid format
    """
    try:
        parse(phone_number)
    except NumberParseException:
        return False
    if len(phone_number) != 12:
        return False
    return True