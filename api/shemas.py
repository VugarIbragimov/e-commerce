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


# class OrderBase(BaseModel):
#     # Добавьте поля, соответствующие вашей модели Order
#     pass


# class OrderCreate(OrderBase):
#     pass


# class Order(OrderBase):
#     # Добавьте поля, соответствующие вашей модели Order

#     class Config:
#         orm_mode = True

# # Аналогично создайте схемы для Address, Favorite и Cart


# class ProductCategoryBase(BaseModel):
#     productId: int
#     categoryId: int


# class ProductCategoryCreate(ProductCategoryBase):
#     pass


# class ProductCategory(ProductCategoryBase):
#     class Config:
#         orm_mode = True
