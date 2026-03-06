# Setup Guide for HydraFit Wellness

Hi! This is your booking system. Here's how to get it running.

## What You'll Need

1. A computer (Windows, Mac, or Linux)
2. About 30 minutes for initial setup
3. Internet connection

---

## Step 1: Install Docker Desktop

1. Go to https://www.docker.com/products/docker-desktop
2. Download for your operating system
3. Install and open Docker Desktop
4. Wait for it to say "Docker is running"

---

## Step 2: Get the Code

**Option A: If you have the code folder**
- Just open it and continue to Step 3

**Option B: Download from GitHub**
1. Go to [the GitHub repository link Tim will send you]
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your Desktop

---

## Step 3: Start the System

### On Windows:
1. Open PowerShell (search for it in Start menu)
2. Navigate to the folder:
```
   cd Desktop\iv-booking-api
```
3. Run:
```
   docker compose up -d
```

### On Mac:
1. Open Terminal (search in Spotlight)
2. Navigate to the folder:
```
   cd Desktop/iv-booking-api
```
3. Run:
```
   docker compose up -d
```

**Wait 1-2 minutes** - Docker is setting up your database and API.

---

## Step 4: Access Your System

Open your web browser and go to:
```
http://localhost:8001/docs
```

You should see the API documentation page!

---

## Step 5: Login as Admin

1. Find **POST /token** in the documentation
2. Click "Try it out"
3. Enter:
   - **username:** `admin`
   - **password:** `admin123`
4. Click "Execute"
5. Copy the `access_token` from the response
6. Click the **"Authorize"** button at the top
7. Paste your token and click "Authorize"

**You're now logged in as admin!**

---

## Daily Use - Checking Today's Schedule

1. Go to http://localhost:8001/docs
2. Login (see Step 5 above)
3. Find **GET /admin/appointments/today**
4. Click "Try it out" → "Execute"
5. See all today's appointments with customer details!

---

## Getting Customer Emails for Marketing

1. Login as admin
2. Find **GET /admin/customers**
3. Click "Try it out" → "Execute"
4. You'll see all customer emails, names, and phone numbers
5. Copy what you need for your email campaigns

---

## Stopping the System

When you're done for the day:
```
docker compose down
```

---

## Restarting Later

Just run:
```
docker compose up -d
```

Everything will be saved - all customers and appointments are in the database.

---

## Need Help?

Text Tim: [your phone number]

---

## What This System Does For You

✅ Customers can book appointments online (no more text message scheduling!)  
✅ Automatic conflict checking (no double bookings)  
✅ Customer database with full history  
✅ View today's schedule instantly  
✅ Export customer emails for marketing  
✅ Track appointment status (scheduled/completed/cancelled)  

---

## Security Notes

- **Change the admin password!** (Tim will show you how)
- Keep Docker Desktop running when you want to use the system
- Your data is stored locally on your computer
- Back up the `iv-booking-api` folder regularly

---

## Next Steps (When Ready)

Phase 2 will add:
- Email confirmations when customers book
- Text message reminders 24 hours before
- Online payment processing
- Customer-facing booking website
- Mobile app

Let Tim know when you want to add these features!