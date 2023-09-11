from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from api.shemas import (DeleteProductResponse, ShowProduct, ProductCreate,
                        ProductInDB, UserCreate,
                        ShowUser, DeleteUserResponse,
                        UpdatedUserResponse, UpdateUserRequest,
                        UpdateProductRequest, UpdatedProductResponse)

from db.dals import ProductDAL

from db.session import get_db
from api.actions.user import (_create_new_user, _delete_user,
                              _get_user_by_id, _update_user)


# ###################### USER ########################### #

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate,
                      db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID,
                      db: AsyncSession = Depends(get_db)
                      ) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404,
                            detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID,
                         db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404,
                            detail=f"User with id {user_id} not found.")
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID, body: UpdateUserRequest,
        db: AsyncSession = Depends(get_db)
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be\
                   provided")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404,
                            detail=f"User with id {user_id} not found.")
    updated_user_id = await _update_user(
        updated_user_params=updated_user_params, db=db, user_id=user_id)
    return UpdatedUserResponse(updated_user_id=updated_user_id)


# ##################### PRODUCT ######################### #

product_router = APIRouter()


async def _get_product_by_id(product_id, db) -> Union[ShowProduct, None]:
    async with db as session:
        async with session.begin():
            product_dal = ProductDAL(session)
            product = await product_dal.get_product_by_id(
                product_id=product_id,
            )
            if product is not None:
                return ShowProduct(
                    product_id=product.product_id,
                    name=product.name,
                    price=product.price,
                    size=product.size,
                    small_description=product.small_description,
                    characteristic=product.characteristic,
                    product_care=product.product_care
                )


async def _delete_product(product_id, db) -> Union[int, None]:
    async with db as session:
        async with session.begin():
            product_dal = ProductDAL(session)
            deleted_product_id = await product_dal.delete_product(
                product_id=product_id,
            )
            return deleted_product_id


async def _update_product(updated_product_params: dict,
                          product_id: int, db) -> Union[int, None]:
    async with db as session:
        async with session.begin():
            product_dal = ProductDAL(session)
            updated_product_id = await product_dal.update_product(
                product_id=product_id,
                **updated_product_params
            )
            return updated_product_id


@product_router.post("/", response_model=ShowProduct)
async def create_product(product_data: ProductCreate,
                         db: AsyncSession = Depends(get_db)):
    async with db.begin():
        product_dal = ProductDAL(db)
        product = await product_dal.create_product(**product_data.dict())
        return product


@product_router.get("/{product_id}", response_model=ShowProduct)
async def get_product_by_id(product_id: int,
                            db: AsyncSession = Depends(get_db)) -> ShowProduct:
    product = await _get_product_by_id(product_id, db)
    if product is None:
        raise HTTPException(status_code=404,
                            detail=f"Product with id {product_id} not found.")
    return product


@product_router.get("/", response_model=ProductInDB)
async def read_all_products(db: AsyncSession = Depends(get_db)):
    product_dal = ProductDAL(db)
    products = await product_dal.get_all_products()
    return products


@product_router.patch("/", response_model=ShowProduct)
async def update__by_id(
        product_id: int, body: UpdateProductRequest,
        db: AsyncSession = Depends(get_db)
) -> UpdatedProductResponse:
    updated_product_params = body.dict(exclude_none=True)
    if updated_product_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for product update info should be\
                   provided")
    product = await _get_product_by_id(product_id, db)
    if product is None:
        raise HTTPException(status_code=404,
                            detail=f"Product with id {product_id} not found.")
    updated_product_id = await _update_product(
        updated_product_params=updated_product_params, db=db,
        product_id=product_id)
    return UpdatedProductResponse(updated_product_id=updated_product_id)


@product_router.delete("/", response_model=DeleteProductResponse)
async def delete_product(product_id: int,
                         db: AsyncSession = Depends(get_db)
                         ) -> DeleteProductResponse:
    deleted_product_id = await _delete_product(product_id, db)
    if deleted_product_id is None:
        raise HTTPException(status_code=404,
                            detail=f"Product with id {product_id} not found.")
    return DeleteProductResponse(deleted_product_id=deleted_product_id)
