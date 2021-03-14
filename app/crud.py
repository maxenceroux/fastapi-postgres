from sqlalchemy.orm import Session

import models, schemas


def get_contact(db: Session, id: int):
    return db.query(models.Contact).filter(models.Contact.id == id).first()


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
