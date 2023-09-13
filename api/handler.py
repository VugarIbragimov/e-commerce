from typing import Union
from uuid import UUID
from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from api.actions.auth import get_current_user_from_token
from sqlalchemy.exc import IntegrityError
from api.actions.user import check_user_permissions

from api.shemas import (DeleteProductResponse, ShowProduct, ProductCreate,
                        ProductInDB, UserCreate,
                        ShowUser, DeleteUserResponse,
                        UpdatedUserResponse, UpdateUserRequest,
                        UpdateProductRequest, UpdatedProductResponse)

from db.dals import ProductDAL
from db.models import User

from db.session import get_db
from api.actions.user import (_create_new_user, _delete_user,
                              _get_user_by_id, _update_user)


# ###################### USER ########################### #

user_router = APIRouter()

logger = getLogger(__name__)


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate,
                      db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID,
                      db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user_from_token)
                      ) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404,
                            detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
        ) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404,
                            detail=f"User with id {user_id} not found.")
    return user


@user_router.patch("/admin_privilege", response_model=UpdatedUserResponse)
async def grant_admin_privilege(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_promotion = await _get_user_by_id(user_id, db)
    if user_for_promotion.is_admin or user_for_promotion.is_superadmin:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {user_id} already\
                promoted to admin / superadmin.",)

    if user_for_promotion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {
        "roles": user_for_promotion.enrich_admin_roles_by_admin_role()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params,
            session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.delete("/admin_privilege", response_model=UpdatedUserResponse)
async def revoke_admin_privilege(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_revoke_admin_privileges = await _get_user_by_id(user_id, db)
    if not user_for_revoke_admin_privileges.is_admin:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {user_id} has no admin privileges."
        )
    if user_for_revoke_admin_privileges is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {
        "roles": user_for_revoke_admin_privileges.remove_admin_privileges_from_model()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params,
            session=db, user_id=user_id)

    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID, body: UpdateUserRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be\
                   provided")
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if user_id != current_user.user_id:
        if check_user_permissions(
            target_user=user_for_update, current_user=current_user
        ):
            raise HTTPException(status_code=403, detail="Forbidden.")
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db,
            user_id=user_id)

    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
    # user = await _get_user_by_id(user_id, db)
    # if user is None:
    #     raise HTTPException(status_code=404,
    #                         detail=f"User with id {user_id} not found.")
    # updated_user_id = await _update_user(
    #     updated_user_params=updated_user_params, db=db, user_id=user_id)
    # return UpdatedUserResponse(updated_user_id=updated_user_id)


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
