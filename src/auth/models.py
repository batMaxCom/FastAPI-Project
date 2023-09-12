from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, BOOLEAN, Boolean
from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTable
from src.database import Base, metadata


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, )
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    type = Column(String, nullable=True, default='buyer')
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    changed_password_date = Column(TIMESTAMP, nullable=True)
    new_email = Column(String, nullable=True)
    code = Column(Integer, nullable=True)
    hashed_password = Column(String(length=1024), nullable=False)


contact = Table(
    "contact",
    metadata,
    Column("user", Integer, ForeignKey("user.id")),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("surname", String, nullable=True),

    Column("region", String, nullable=False),
    Column("area", String, nullable=True),
    Column("city", String, nullable=False),

    Column("street", String, nullable=False),

    Column("house", String, nullable=False),
    Column("structure", String, nullable=True),
    Column("building", String, nullable=True),
    Column("apartment", String, nullable=True),
    Column("phone", Integer, nullable=False)
)


