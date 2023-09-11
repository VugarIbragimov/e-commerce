from typing import Union
from uuid import UUID

from fastapi import HTTPException

from db.models import User, UserRole
from hashing import Hasher
from api.shemas import UserCreate, ShowUser
from db.dals import UserDAL


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
                phone_number=body.phone_number,
                hashed_password=Hasher.get_password_hash(body.hashed_password),
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                phone_number=user.phone_number,
            )


async def _delete_user(user_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(
                user_id=user_id,
            )
            return deleted_user_id


async def _update_user(
    updated_user_params: dict, user_id: UUID, db
) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(
                user_id=user_id, **updated_user_params
            )
            return updated_user_id


async def _get_user_by_id(user_id, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return user


def check_user_permissions(target_user: User, current_user: User) -> bool:
    if UserRole.ROLE_SUPERADMIN in current_user.roles:
        raise HTTPException(
            status_code=406, detail="Superadmin cannot be deleted via API."
        )
    if target_user.user_id != current_user.user_id:
        # check admin role
        if not {
            UserRole.ROLE_ADMIN,
            UserRole.ROLE_SUPERADMIN,
        }.intersection(current_user.roles):
            return False
        # check admin deactivate superadmin attempt
        if (
            UserRole.ROLE_SUPERADMIN in target_user.roles
            and UserRole.ROLE_ADMIN in current_user.roles
        ):
            return False
        # check admin deactivate admin attempt
        if (
            UserRole.ROLE_ADMIN in target_user.roles
            and UserRole.ROLE_ADMIN in current_user.roles
        ):
            return False
    return True
