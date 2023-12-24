import re
import uuid
# from typing import Optional

# from fastapi import HTTPException
from pydantic import BaseModel
# from pydantic import constr
from pydantic import EmailStr
# from pydantic import validator

#########################
# BLOCK WITH API MODELS #
#########################

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        from_attributes = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
