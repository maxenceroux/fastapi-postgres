from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/contact", response_model=schemas.ContactSchema)
def create_contact(contact: schemas.ContactSchema, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_contact_id(db, contact_id=contact.contact_id)
    if db_contact:
        raise HTTPException(status_code=400, detail="Contact already in db")
    return crud.create_contact(db=db, contact=contact)


@app.post("/contacts", response_model=schemas.ContactsSchema)
def create_contacts(contacts: schemas.ContactsSchema, db: Session = Depends(get_db)):
    for ct in contacts.contacts:
        db_contact = crud.get_contact_by_contact_id(db, contact_id=ct.contact_id)
        if db_contact:
            raise HTTPException(status_code=400, detail="Contact already in db")
        crud.create_contact(db=db, contact=ct)
    return contacts


@app.get("/contacts")
def get_contact(db: Session = Depends(get_db)):
    return crud.get_contacts(db=db)