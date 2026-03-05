from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, EmailStr, ConfigDict
from starlette.status import HTTP_201_CREATED

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

class AppointmentCreate(BaseModel):
    service_id: int
    appointment_date: datetime
    notes: Optional[str] = None

class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    service_id: int
    appointment_date: datetime
    status: str
    notes: Optional[str]
    created_at: datetime

    service: ServiceResponse

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


#Appointment Endpoints
@app.post("/appointments", response_model=AppointmentResponse, status_code=HTTP_201_CREATED)
def create_appointment(
        appointment:AppointmentCreate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    service = db.query(models.Service).filter(models.Service.id==appointment.service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    exisitng = db.query(models.Appointment).filter(
        models.Appointment.appointment_date == appointment.appointment_date,
        models.Appointment.status == models.AppointmentStatus.scheduled
    ).first()

    if exisitng:
        raise HTTPException(status_code=400, detail="Time slot already booked")

    db_appointment = models.Appointment(
        user_id = current_user.id,
        service_id = appointment.service_id,
        appointment_date = appointment.appointment_date,
        notes = appointment.notes
    )

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.get('/appointments/my', response_model=List[AppointmentResponse])
def get_my_appointments(
        current_user: models.User =Depends(get_current_user),
        db: Session = Depends(get_db)
):
    appointments = db.query(models.Appointment).filter(
        models.Appointment.user_id == current_user.id
    ).order_by(models.Appointment.appointment_date.desc()).all()
    return appointments

@app.delete('/appointments/{appointment_id}')
def cancel_appointment(
        appointment_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id,
        models.Appointment.user_id == current_user.id
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = models.AppointmentStatus.canceled
    db.commit()
    return {"message": "Appointment canceled", "id": appointment_id}

#Admin helper function
def verify_admin(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

#Admin Endpoints
@app.get("/admin/appointments/today", response_model=List[AppointmentResponse])
def get_todays_appointments(
        admin: models.User = Depends(verify_admin),
        db: Session = Depends(get_db)
):
    from datetime import date as dt_date
    today = dt_date.today()

    appointments = db.query(models.Appointment).filter(
        models.Appointment.appointment_date >= datetime.combine(today, datetime.min.time()),
        models.Appointment.appointment_date < datetime.combine(today, datetime.max.time()),
        models.Appointment.status == models.AppointmentStatus.scheduled
    ).order_by(models.Appointment.appointment_date).all()

    return appointments

@app.get("/admin/appointments/all", response_model=List[AppointmentResponse])
def get_all_appointments(
        admin: models.User = Depends(verify_admin),
        db: Session = Depends(get_db)
):
    appointments = db.query(models.Appointment).order_by(
        models.Appointment.appointment_date.desc()
    ).all()
    return appointments

@app.get("/admin/customers", response_model=List[UserResponse])
def get_customers(
        admin: models.User = Depends(verify_admin),
        db: Session = Depends(get_db)
):
    customers = db.query(models.User).filter(
        models.User.is_admin == False
    ).all()
    return customers