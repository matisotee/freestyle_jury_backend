from pydantic import BaseModel, EmailStr
from typing import Union


class User(BaseModel):

    id: Union[str, None] = None
    provider_id: str
    name: str
    last_name: str
    email: EmailStr
    phone_number: str = ''
    aka: str = ''


class UserExternalRepresentation(BaseModel):
    id: str
    name: str
    last_name: str
    email: EmailStr
    phone_number: str = ''
    aka: str = ''
