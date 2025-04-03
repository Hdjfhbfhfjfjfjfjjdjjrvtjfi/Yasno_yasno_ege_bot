__all__ = ["UserData"]
from phonenumbers import parse, NumberParseException

from aiogram.types import Message

from pydantic import BaseModel, ConfigDict
from pydantic import field_validator


class UserData(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    user_id: int
    name_last_name_surname: str | None = None
    phone_number: str | None = None
    last_message: Message | None = None

    @field_validator('phone_number')
    def phone_number_is_valid(cls, phone_number: str) -> str:
        try:
            number = parse(phone_number)
        except NumberParseException:
            raise ValueError(f'Invalid phone number: {phone_number}')
        number = f"+{number.country_code}{number.national_number}"
        return number

    @field_validator('phone_number')
    def phone_number_length_is_valid(cls, phone_number: str) -> str:
        if len(phone_number) != 12:
            raise ValueError(f'Invalid phone number: {phone_number}')
        return phone_number

    @field_validator('name_last_name_surname')
    def full_name_is_valid(cls, full_name: str) -> str:
        if len(full_name.split()) != 3:
            raise ValueError(f'Invalid full name: {full_name}')
        else:
            return full_name
