from pydantic import BaseModel, ValidationError, validator


class UserDTO(BaseModel):
    email: str
    password: str
    username: str

    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValidationError("Must be a valid email")
        return v

    @validator("password")
    def validate_password(cls, v):
        if not len(v) >= 8:
            raise ValidationError("The password must have at least 8 characters")
        return v

    @validator("username")
    def validate_username(cls, v):
        if not len(v) >= 5:
            raise ValidationError("The username must have at least 5 characters")
        return v
