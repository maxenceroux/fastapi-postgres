from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    contact_id = Column(Integer, unique=True, index=True)
