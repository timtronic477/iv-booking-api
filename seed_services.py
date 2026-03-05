from database import SessionLocal, engine, Base
from models import Service
from decimal import Decimal


Base.metadata.create_all(bind=engine)

db = SessionLocal()

exisiting = db.query(Service).first()
if exisiting:
    print("Services already seeded!")
    db.close()
    exit()

services = [
    # IV Therapy
    {"name": "Myers Cocktail", "description": "Energy boost, immunity support", "price": Decimal("150.00"),
     "duration_minutes": 45, "category": "IV Therapy"},
    {"name": "Immunity Boost", "description": "Strengthen immune system", "price": Decimal("150.00"),
     "duration_minutes": 45, "category": "IV Therapy"},
    {"name": "Energy Boost", "description": "Combat fatigue", "price": Decimal("150.00"), "duration_minutes": 45,
     "category": "IV Therapy"},
    {"name": "Hangover Relief", "description": "Rapid recovery", "price": Decimal("150.00"), "duration_minutes": 45,
     "category": "IV Therapy"},
    {"name": "Beauty Glow", "description": "Skin health and radiance", "price": Decimal("175.00"),
     "duration_minutes": 45, "category": "IV Therapy"},
    {"name": "Athletic Performance", "description": "Recovery and endurance", "price": Decimal("175.00"),
     "duration_minutes": 45, "category": "IV Therapy"},
    {"name": "Custom IV", "description": "Personalized blend", "price": Decimal("200.00"), "duration_minutes": 60,
     "category": "IV Therapy"},

    # Add-ons
    {"name": "Glutathione Push", "description": "Antioxidant boost", "price": Decimal("50.00"), "duration_minutes": 15,
     "category": "Add-ons"},
    {"name": "B12 Shot", "description": "Energy enhancement", "price": Decimal("25.00"), "duration_minutes": 15,
     "category": "Add-ons"},
    {"name": "Vitamin D Shot", "description": "Bone and immune health", "price": Decimal("25.00"),
     "duration_minutes": 15, "category": "Add-ons"},
]

for service_data in services:
    service = Service(**service_data)
    db.add(service)

db.commit()
print(f"Added {len(services)} services!")
db.close()