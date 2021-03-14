from sqlalchemy.orm import Session

import models, schemas
from werkzeug.security import generate_password_hash


def get_contact_by_contact_id(db: Session, contact_id: str):
    return (
        db.query(models.Contact).filter(models.Contact.contact_id == contact_id).first()
    )


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schemas.ContactSchema):
    db_contact = models.Contact(contact_id=contact.contact_id, email=contact.email)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def create_user(db: Session, user: schemas.UserSchema):
    db_user = models.User(
        username=user.username, password=generate_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    return db_user


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_contact(db: Session, contact_id: int):
    return (
        db.query(models.Contact).filter(models.Contact.contact_id == contact_id).first()
    )
