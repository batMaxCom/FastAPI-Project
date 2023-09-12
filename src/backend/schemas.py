from datetime import datetime

from pydantic import BaseModel


class ShopCreate(BaseModel):
	id: int
	url: str
	filename: str
	user_id: int


class ShopList(BaseModel):
	id: int
	url: str
	filename: str
	user_id: int
	last_update: datetime

	class Config:
		orm_mode = True


class CategoryList(BaseModel):
	id: int
	shop: int
	name: str

	class Config:
		orm_mode = True


class ProductList(BaseModel):
	id: int
	category: int
	name: str

	class Config:
		orm_mode = True
