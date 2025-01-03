from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import connection
from src.product.repository import ProductRepository


class ProductService:

    @staticmethod
    @connection
    async def get_products(session: AsyncSession):
        result = await ProductRepository.find_all(session)
        return result

    @staticmethod
    @connection
    async def get_product_by_id(product_id: int, session: AsyncSession):
        result = await ProductRepository.find_one_or_none(session, product_id)
        return result

    @staticmethod
    @connection
    async def add_product(product: dict, session: AsyncSession):
        result = await ProductRepository.add_one(session, product)
        return result

    @staticmethod
    @connection
    async def update_product_by_id(product_id: int, product: dict, session: AsyncSession):
        result = await ProductRepository.update_one(session, product_id, product)
        return result

    @staticmethod
    @connection
    async def delete_product_by_id(product_id: int, session: AsyncSession):
        result = await ProductRepository.delete_one(session, product_id)
        return result

    @staticmethod
    @connection
    async def get_purchase_info(session: AsyncSession, product_id: int | None = None):
        result = await ProductRepository.get_purchase_info(session, product_id)
        return result

    @staticmethod
    @connection
    async def get_stock_info(session: AsyncSession, product_name: str):
        result = await ProductRepository.get_stock_info(session, product_name)
        return result

    @staticmethod
    @connection
    async def get_all_stock_info(session: AsyncSession, price_filter: dict | None = None):
        result = await ProductRepository.get_all_stock_info(session, price_filter)
        return result

    @staticmethod
    @connection
    async def get_statistics(session: AsyncSession):
        result = await ProductRepository.get_statistics(session)
        return result


class ProductTypeService:

    @staticmethod
    @connection
    async def get_all_product_types(session: AsyncSession):
        result = await ProductRepository.find_all(session)
        return result

