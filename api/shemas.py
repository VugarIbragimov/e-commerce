import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import validator

#########################
# BLOCK WITH API MODELS #
#########################

# ###################### USER ########################### #

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    phone_number: str


class UserCreate(BaseModel):

    name: str
    surname: str
    email: EmailStr
    phone_number: str
    hashed_password: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]
    phone_number: Optional[constr(min_length=1)]

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class Token(BaseModel):
    access_token: str
    token_type: str

# ##################### PRODUCT ######################### #


class ProductCreate(BaseModel):
    name: str
    price: float
    size: str
    small_description: str
    characteristic: str
    product_care: str


class ShowProduct(TunedModel):
    product_id: int
    name: str
    price: float
    size: str
    small_description: str
    characteristic: str
    product_care: str


class DeleteProductResponse(BaseModel):
    deleted_product_id: int


class UpdatedProductResponse(BaseModel):
    updated_product_id: int


class UpdateProductRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    price: float
    size: Optional[constr(min_length=1)]
    small_description: Optional[constr(min_length=1)]
    characteristic: Optional[constr(min_length=1)]
    product_care: Optional[constr(min_length=1)]


class ProductInDB(BaseModel):
    product_id: int
    name: str
    price: float
    size: str
    small_description: str
    characteristic: str
    product_care: str


# ##################### CATEGORY ######################### #
