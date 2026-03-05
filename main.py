from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, EmailStr, ConfigDict

from database import get_db, Base, engine
from auth import get_current_user, get_password_hash, create_access_token, verify_password
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hydrafit Wellness Booking API")

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    phone: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    username: str
    phone: Optional[str]
    is_admin: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    duration_minutes: int
    category: str
    is_active: bool

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail='Email already registered')
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail='Username already registered')

    db_user = models.User(
        email = user.email,
        username = user.username,
        phone = user.phone,
        hashed_password = get_password_hash(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/services", response_model=List[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    services = db.query(models.Service).filter(models.Service.is_active == True).all()
    return services

@app.get("/services/{service_id}", response_model= ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service