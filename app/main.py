from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
JWT_SECRET = "mysecret"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@app.post("/token", status_code=200)
def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return {"error": "invalid credentials"}
    token = jwt.encode({"user": user.username}, JWT_SECRET)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/contact", response_model=schemas.ContactSchema)
def create_contact(
    contact: schemas.ContactSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    db_contact = crud.get_contact_by_contact_id(db, contact_id=contact.contact_id)
    if db_contact:
        raise HTTPException(status_code=400, detail="Contact already in db")
    return crud.create_contact(db=db, contact=contact)


@app.post("/contacts", response_model=schemas.ContactsSchema)
def create_contacts(
    contacts: schemas.ContactsSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    for ct in contacts.contacts:
        db_contact = crud.get_contact_by_contact_id(db, contact_id=ct.contact_id)
        if db_contact:
            raise HTTPException(status_code=400, detail="Contact already in db")
        crud.create_contact(db=db, contact=ct)
    return contacts


@app.get("/contact/{contact_id}", response_model=schemas.ContactSchema)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_contact


@app.get("/user/{username}", response_model=schemas.UserSchema)
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_user.check_password(password):
        return False
    return db_user


@app.get("/contacts")
def get_contact(db: Session = Depends(get_db)):
    return crud.get_contacts(db=db)


@app.post("/user/", response_model=schemas.UserSchema)
def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)
