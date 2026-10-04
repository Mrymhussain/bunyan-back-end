from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserRegistrationSchema(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialty: Optional[str] = None


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    role: str
    specialty: Optional[str] = None
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserTokenSchema(BaseModel):
    token: str
    message: str