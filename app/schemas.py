from typing import List, Optional


from pydantic import BaseModel


class ContactSchema(BaseModel):
    email: str
    contact_id: int

    class Config:
        orm_mode = True


class ContactsSchema(BaseModel):
    contacts: List[ContactSchema]

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
