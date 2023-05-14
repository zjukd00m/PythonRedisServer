from pydantic import BaseModel, validator, ValidationError


class LoginDTO(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValidationError("Must be a valid email")
        return v
