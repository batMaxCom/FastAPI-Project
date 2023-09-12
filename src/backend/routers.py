from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.models import shop, category, product
from src.backend.schemas import ShopCreate, ShopList, CategoryList, ProductList
from src.database import get_async_session

router = APIRouter(
    prefix="/api/v1",
    tags=["Backend"]
)

@router.post("/shop")
async def create_shop(new_shop: ShopCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(shop).values(**new_shop.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/shop", response_model=List[ShopList])
async def shop_list(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(shop)
    result = await session.execute(query)
    return result.all()

@router.get("/category", response_model=List[CategoryList])
async def category_list(session: AsyncSession = Depends(get_async_session)):
    query = select(category)
    result = await session.execute(query)
    return result.all()

@router.get("/product", response_model=List[ProductList])
async def product_list(session: AsyncSession = Depends(get_async_session)):
    query = select(product)
    result = await session.execute(query)
    return result.all()
