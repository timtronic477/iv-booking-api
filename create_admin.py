from database import SessionLocal
from models import User
from auth import get_password_hash

db = SessionLocal()

admin = db.query(User).filter(User.is_admin == True).first()
if admin:
    print(f"Admin already exists: {admin.username}")
else:
    admin = User(
        email="admin@hydrafit.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    print("Admin created! Username: admin, Password: admin123")

db.close()