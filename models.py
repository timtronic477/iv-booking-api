from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at= Column(DateTime(timezone=True), server_default = func.now())

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default = func.now())

class AppointmentStatus(enum.Enum):
    scheduled = "scheduled"
    completed = 'completed'
    canceled = 'canceled'
    no_show = 'no_show'

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    appointment_date = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(SQLEnum(AppointmentStatus),default=AppointmentStatus.scheduled)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(String, nullable=True)

    user = relationship("User", backref="appointments")
    service = relationship("Service", backref="appointments")
