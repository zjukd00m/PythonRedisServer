from pydantic import BaseModel, validator, ValidationError
from typing import Optional
from uuid import UUID
import re

UUID_REGEX = re.compile(
    "^[0-9a-f]{8}-[0-9a-f]{4}-[4-9a-f]{4}-[89ab-cd ef]{3}-[0-9a-f]{12}$"
)


class BaseUserDTO(BaseModel):
    username: str
    email: str

    @validator("username")
    def validate_username(cls, v):
        if len(v) < 5:
            raise ValidationError("Username must have at least 5 characters")
        return v

    @validator("email")
    def validate_email(cls, v):
        return v


class UserDTO(BaseUserDTO):
    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValidationError("Password must have at least 8 characters")
        return v


class UpdateUserDTO(BaseModel):
    username: Optional[str]
    email: Optional[str]

    @validator("username")
    def validate_username(cls, v):
        if len(v) < 5:
            raise ValidationError("Username must have at least 5 characters")
        return v

    @validator("email")
    def validate_email(cls, v):
        return v


class UserIDDTO(BaseModel):
    user_id: UUID

    @validator("user_id")
    def validate_user_id(cls, v):
        try:
            UUID(v, version=4)
            return v
        except ValueError:
            raise ValidationError("Invalid UUID")


class SearchUsersDTO(BaseModel):
    user_id: Optional[UUID]
    username: Optional[str]
    email: Optional[str]
