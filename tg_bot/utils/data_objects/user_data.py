__all__ = ["UserData"]
from aiogram.types import Message

from phonenumbers import parse, NumberParseException

from pydantic import BaseModel, ConfigDict
from pydantic import field_validator


class UserData(BaseModel):
    """Data class for storing and validating user information.

    This class represents user data with validation for phone numbers and full names.
    It uses Pydantic for data validation and serialization.

    :ivar user_id: The user's unique identifier
    :ivar name_last_name_surname: The user's full name
    :ivar phone_number: The user's phone number
    :ivar last_message: Last related message from the bot
    """
    model_config = ConfigDict(validate_assignment=True)
    user_id: int
    name_last_name_surname: str | None = None
    phone_number: str | None = None
    last_message: Message | None = None

    @field_validator('phone_number')
    def phone_number_is_valid(cls, phone_number: str) -> str:
        """Validates that the phone number is in a valid format.

        :param phone_number: The phone number to validate
        :return: The normalized phone number in international format
        :raise ValueError: If the phone number is not in a valid format
        """
        try:
            number = parse(phone_number)
        except NumberParseException:
            raise ValueError(f'Invalid phone number: {phone_number}')
        number = f"+{number.country_code}{number.national_number}"
        return number

    @field_validator('phone_number')
    def phone_number_length_is_valid(cls, phone_number: str) -> str:
        """Validates that the phone number has the correct length.

        :param phone_number: The phone number to validate
        :return: The validated phone number
        :raise ValueError: If the phone number length is not 12 characters
        """
        if len(phone_number) != 12:
            raise ValueError(f'Invalid phone number: {phone_number}')
        return phone_number

    @field_validator('name_last_name_surname')
    def full_name_is_valid(cls, full_name: str) -> str:
        """Validates that the full name contains exactly three parts (name, last name, surname).

        :param full_name: The full name to validate
        :return: The validated full name
        :raise ValueError: If the full name does not contain exactly three parts
        """
        if len(full_name.split()) != 3:
            raise ValueError(f'Invalid full name: {full_name}')
        else:
            return full_name
