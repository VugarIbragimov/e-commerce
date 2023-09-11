from uuid import UUID
from typing import Union, List

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Product


###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


# ###################### USER ########################### #


class UserDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def create_user(self, name: str, surname: str,
                          email: str, phone_number: str,
                          hashed_password: str) -> User:

        new_user = User(
            name=name,
            surname=surname,
            email=email,
            phone_number=phone_number,
            hashed_password=hashed_password)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = update(User). \
            where(and_(User.user_id == user_id, User.is_active == True)). \
            values(kwargs). \
            returning(User.user_id)
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = update(User).\
            where(and_(User.user_id == user_id, User.is_active == True)).\
            values(is_active=False).returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


# ##################### PRODUCT ######################### #


class ProductDAL:
    """Data Access Layer for operating product info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_product_by_id(self, product_id: int) -> Union[Product, None]:
        query = select(Product).where(Product.product_id == product_id)
        res = await self.db_session.execute(query)
        product = res.fetchone()
        return product[0]

    async def get_all_products(self) -> List[Product]:
        query = select(Product)
        res = await self.db_session.execute(query)
        products = res.fetchall()
        return products

    async def create_product(self, name: str, price: float,
                             small_description: str, size: str,
                             characteristic: str,
                             product_care: str) -> Product:
        new_product = Product(name=name, price=price,
                              small_description=small_description,
                              size=size, characteristic=characteristic,
                              product_care=product_care)
        self.db_session.add(new_product)
        await self.db_session.flush()
        return new_product

    async def update_product(self, product_id: int,
                             **kwargs) -> Union[int, None]:
        query = update(Product). \
            where(Product.product_id == product_id). \
            values(kwargs). \
            returning(Product.product_id)
        res = await self.db_session.execute(query)
        updated_product_id = res.fetchone()
        return updated_product_id[0]

    async def delete_product(self, product_id: int) -> Union[int, None]:
        query = delete(Product).\
            where(Product.product_id == product_id).\
            returning(Product.product_id)
        res = await self.db_session.execute(query)
        deleted_product_id = res.fetchone()
        return deleted_product_id[0]
