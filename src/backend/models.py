from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, BOOLEAN, text, DateTime, \
    func

from src.auth.models import User
from src.database import metadata

shop = Table(
    "shop",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String, nullable=True),
    Column("filename", String, nullable=True),
    Column("last_update", TIMESTAMP, default=datetime.utcnow),
    Column("user_id", Integer, ForeignKey(User.id)),
)

category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("shop", Integer, ForeignKey("shop.id"), nullable=False),
    Column("name", String, nullable=False)
)

product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("category", Integer, ForeignKey("category.id")),
    Column("name", String, nullable=False)
)
