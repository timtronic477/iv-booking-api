# HydraFit Wellness - IV Therapy Booking System

A complete booking and customer management system for IV therapy businesses. Built for HydraFit Wellness to replace manual scheduling and enable online bookings.

## 🎯 Problem Solved

**Before:** Bookings managed through text messages and paper calendar
- Double bookings
- No customer history
- Manual mailing list management
- Time-consuming admin work

**After:** Professional booking system
- Automated conflict checking
- Customer database with full history
- Easy customer list export for marketing
- Admin dashboard for daily schedule

---

## ✨ Features

### For Customers
- ✅ Create account with email/phone
- ✅ Browse available IV therapy services
- ✅ Book appointments online
- ✅ View booking history
- ✅ Cancel appointments

### For Admin (Business Owner)
- ✅ View today's schedule at a glance
- ✅ See all upcoming appointments
- ✅ Access customer database
- ✅ Export customer emails for marketing
- ✅ Track appointment status (scheduled/completed/cancelled/no-show)

### Services Offered
- Myers Cocktail - $150 (45 min)
- Immunity Boost - $150 (45 min)
- Energy Boost - $150 (45 min)
- Hangover Relief - $150 (45 min)
- Beauty Glow - $175 (45 min)
- Athletic Performance - $175 (45 min)
- Custom IV - $200 (60 min)
- Add-ons: Glutathione, B12 Shot, Vitamin D Shot

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **Authentication:** JWT tokens with bcrypt password hashing
- **ORM:** SQLAlchemy
- **Containerization:** Docker & Docker Compose
- **API Documentation:** Auto-generated with OpenAPI/Swagger

---

## 📋 API Endpoints

### Authentication
- `POST /register` - Create customer account
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user info

### Services
- `GET /services` - List all active services
- `GET /services/{id}` - Get service details

### Appointments (Customer)
- `POST /appointments` - Book appointment
- `GET /appointments/my` - View my appointments
- `DELETE /appointments/{id}` - Cancel appointment

### Admin Endpoints (Requires admin role)
- `GET /admin/appointments/today` - Today's schedule
- `GET /admin/appointments/all` - All appointments
- `GET /admin/customers` - Customer list with emails

---

## 🚀 Local Setup

### Prerequisites
- Docker Desktop installed
- Git

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/iv-booking-api.git
   cd iv-booking-api
```

2. **Start the application**
```bash
   docker compose up --build
```

3. **Access the API**
   - API Documentation: http://localhost:8001/docs
   - API Base URL: http://localhost:8001

4. **Create admin account** (first time only)
```bash
   docker compose exec web python create_admin.py
```
   Default admin credentials: `admin` / `admin123`

5. **Seed services** (first time only)
```bash
   docker compose exec web python seed_services.py
```

---

## 📱 Using the API

### Customer Flow

1. **Register** → `POST /register`
2. **Login** → `POST /token` (get your access token)
3. **Authorize** → Click "Authorize" in `/docs`, paste token
4. **Browse Services** → `GET /services`
5. **Book Appointment** → `POST /appointments`
6. **View Bookings** → `GET /appointments/my`

### Admin Flow

1. **Login as admin** → `POST /token`
2. **View today's schedule** → `GET /admin/appointments/today`
3. **See all customers** → `GET /admin/customers`
4. **Manage appointments** → `GET /admin/appointments/all`

---

## 🗄 Database Schema
```
users
├── id (Primary Key)
├── email (Unique)
├── username (Unique)
├── hashed_password
├── phone
├── is_admin (Boolean)
└── created_at

services
├── id (Primary Key)
├── name
├── description
├── price (Decimal)
├── duration_minutes
├── category
├── is_active
└── created_at

appointments
├── id (Primary Key)
├── user_id (Foreign Key → users)
├── service_id (Foreign Key → services)
├── appointment_date
├── status (Enum: scheduled/completed/cancelled/no_show)
├── notes
├── created_at
└── updated_at
```

---

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control (customer vs admin)
- Protected admin endpoints
- SQL injection prevention via SQLAlchemy ORM

---

## 📈 Future Enhancements (Phase 2)

- [ ] Email notifications (booking confirmations, reminders)
- [ ] SMS reminders (24 hours before appointment)
- [ ] Package deals (buy 5, get 1 free)
- [ ] Customer intake forms (medical history, allergies)
- [ ] Payment processing (Stripe integration)
- [ ] Calendar view for available time slots
- [ ] Mobile app or customer-facing web interface
- [ ] Revenue analytics dashboard
- [ ] Gift certificate system
- [ ] Referral tracking

---

## 👨‍💻 Developer

**Timothy Balilo**
- GitHub: [@timtronic477](https://github.com/timtronic477)
- LinkedIn: [Timothy Balilo](https://linkedin.com/in/Timothy-Balilo)

**Built for:** HydraFit Wellness IV Therapy

---

## 📄 License

MIT License - This project was built as a real business solution and portfolio project.

---

## 🙏 Acknowledgments

Built to solve a real business problem for HydraFit Wellness, a mobile IV therapy service helping clients optimize their health and wellness.