# 🚀 TravelGo Quick Start Guide - Email & Vehicle Rentals

## Prerequisites

- Python 3.8+
- MongoDB 4.4+
- pip (Python Package Manager)
- A Gmail account (for email testing)

---

## 5-Minute Setup

### Step 1: Install Required Packages

```bash
pip install -r requirements.txt
```

This installs:
- `Flask==2.3.2` - Web framework
- `Flask-Mail==0.9.1` - Email notifications
- `boto3==1.34.162` - AWS DynamoDB database access
- `python-dateutil==2.8.2` - Date handling
- All other dependencies

### Step 2: Configure Email (Gmail)

#### 2a. Enable 2-Factor Authentication
1. Go to [Google Account](https://myaccount.google.com)
2. Click "Security" in the left menu
3. Enable "2-Step Verification"

#### 2b. Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Windows Computer"
3. Google generates a 16-character password
4. **Copy this password**

#### 2c. Create `.env` File

In your project root directory, create `.env`:

```bash
# Copy from .env.example
cp .env.example .env
```

Edit `.env` and update:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx  # Paste the 16-char password here
MAIL_DEFAULT_SENDER=noreply@travelgo.com
```

### Step 3: Start the Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 4: Test the Features

#### Test Welcome Email
1. Open http://localhost:5000/register
2. Create a new account
3. Check your inbox for welcome email ✅

#### Test Vehicle Rentals
1. Log in to your account
2. Click "🚗 Vehicles" in the navigation
3. Search for vehicles by location and dates
4. Click "Book Now" and complete the booking
5. Check your inbox for booking confirmation email ✅

---

## File Overview

### New Files Created

| File | Purpose |
|------|---------|
| `templates/vehicles.html` | Vehicle search/listing page |
| `templates/vehicle_details.html` | Detailed vehicle information |
| `VEHICLES_SETUP.md` | Complete vehicle rental documentation |
| `EMAIL_SETUP.md` | Complete email system documentation |
| `.env.example` | Environment configuration template |

### Modified Files

| File | Changes |
|------|---------|
| `app.py` | Added email config + 4 vehicle routes + 3 email functions |
| `requirements.txt` | Added Flask-Mail, python-dateutil, Pillow |
| `templates/dashboard.html` | Added vehicle link to navigation & features |

---

## Routes Reference

### Vehicle Routes

```
GET/POST  /vehicles                    - Search and list vehicles
GET       /vehicle-details/<id>        - View vehicle details
POST      /book-vehicle                - Process vehicle booking
```

### Email Functions (Internal)

```
send_welcome_email(email, name)
send_booking_confirmation_email(email, name, booking)
send_special_offer_email(email, name, title, description, discount)
```

---

## Common Tasks

### Add More Vehicles

Edit the `/vehicles` route in `app.py`:

```python
vehicles_list = [
    # ... existing vehicles ...
    {
        "id": str(uuid.uuid4()),
        "name": "Tesla Model 3",
        "type": "Electric",
        "price": "$55",
        "image": "⚡",
        "transmission": "Automatic",
        "passengers": "5",
        "luggage": "2 bags",
        "fuel": "Electric",
        "rating": "4.9",
        "mileage": "Unlimited"
    }
]
```

### Customize Email Template

Edit `send_booking_confirmation_email()` in `app.py`:

```python
msg.html = """
<html>
<body style="font-family: Poppins; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);">
    <h1 style="color: #00d4ff;">Your Custom Email Here</h1>
    <!-- Update your email content -->
</body>
</html>
"""
```

### Send Test Email

```python
# In Python console
from app import app, send_welcome_email

with app.app_context():
    send_welcome_email("test@example.com", "Test User")
    print("Email sent!")
```

### Check Email Logs

```python
# In Python console
from app import app
from database.db import db

# View recent emails
logs = db["email_logs"].find().sort("timestamp", -1).limit(10)
for log in logs:
    print(log)
```

---

## Troubleshooting

### Email Not Sending

**Error: `SMTPAuthenticationError`**

✅ **Fix:**
- Double-check email and password in `.env`
- Verify 2-Factor Authentication is enabled on Gmail
- Use app password (not account password)
- Check MAIL_SERVER and MAIL_PORT are correct

**Test SMTP connection:**
```python
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'app-password')
print("Success!")
```

### Vehicles Not Showing

**Error: No vehicles in search results**

✅ **Fix:**
- Verify database connection
- Check sample data is loaded
- Restart Flask app
- Verify template syntax

```python
# Test in Python console
from database.db import db
vehicles = list(db["vehicles"].find())
print(vehicles)
```

### Session/Login Issues

**Error: Page redirects to login on vehicle page**

✅ **Fix:**
- Ensure you're logged in
- Check session cookie is set
- Clear browser cookies
- Try in incognito mode

---

## Next Steps

### Deploy to Production

1. Create production `.env` with real credentials
2. Set `FLASK_ENV=production`
3. Use production email service (SendGrid, Mailgun, AWS SES)
4. Enable HTTPS
5. Set up database backups
6. Configure error logging

### Add More Features

* 💳 **Payment Integration** - Add Stripe/PayPal
* 📸 **Vehicle Images** - Upload vehicle photos
* 📱 **SMS Notifications** - Twilio integration
* 📊 **Analytics Dashboard** - Track bookings
* 🔔 **Push Notifications** - Real-time alerts
* ⭐ **Ratings & Reviews** - Customer feedback

### Performance Optimization

* 🚀 **Async Emails** - Background email sending
* 🗄️ **Database Indexing** - Query optimization
* 💾 **Caching** - Redis for frequently accessed data
* 📦 **CDN** - Static file delivery
* ⚡ **API Rate Limiting** - Prevent abuse

---

## Directory Structure

```
Travelgo/
├── app.py                              # Main Flask application
├── config.py                           # Configuration
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment template
│
├── database/
│   ├── db.py                          # Database connection
│   └── __pycache__/
│
├── templates/
│   ├── index.html                     # Home page
│   ├── dashboard.html                 # Dashboard (updated)
│   ├── login.html                     # Login page
│   ├── register.html                  # Registration page
│   ├── vehicles.html                  # Vehicle search (NEW)
│   ├── vehicle_details.html           # Vehicle details (NEW)
│   ├── hotels.html                    # Hotel booking
│   ├── flights.html                   # Flight search
│   ├── bookings.html                  # Booking history
│   ├── profile.html                   # User profile
│   └── [other templates...]
│
├── static/
│   ├── css/
│   │   └── style.css                 # Stylesheet
│   └── js/
│       └── script.js                 # JavaScript
│
├── VEHICLES_SETUP.md                  # Vehicle rental docs (NEW)
├── EMAIL_SETUP.md                     # Email system docs (NEW)
├── README.md                          # Main readme
└── __pycache__/
```

---

## Environment Variables Checklist

✅ Required for Email:
- [ ] `MAIL_SERVER=smtp.gmail.com`
- [ ] `MAIL_PORT=587`
- [ ] `MAIL_USE_TLS=True`
- [ ] `MAIL_USERNAME=your-email@gmail.com`
- [ ] `MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx`
- [ ] `MAIL_DEFAULT_SENDER=noreply@travelgo.com`

✅ Required for Database:
- [ ] MongoDB installed and running
- [ ] Database connection working

✅ Optional:
- [ ] `FLASK_ENV=development`
- [ ] `FLASK_DEBUG=True`

---

## Testing Checklist

- [ ] Register new user (should receive welcome email)
- [ ] Log in successfully
- [ ] Navigate to vehicles page
- [ ] Search vehicles with filters
- [ ] View vehicle details
- [ ] Complete vehicle booking
- [ ] Receive booking confirmation email
- [ ] View booking in booking history
- [ ] Email styling looks good
- [ ] All links work correctly
- [ ] Mobile-responsive design working

---

## API Testing with cURL

### Test Email Endpoint (if available)

```bash
curl -X POST http://localhost:5000/send-test-email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "name": "Test User"}'
```

### Test Vehicle Search

```bash
curl -X POST http://localhost:5000/vehicles \
  -d "location=New York&pickup_date=2024-01-15&return_date=2024-01-20&vehicle_type=economy"
```

---

## Important Security Notes

⚠️ **Never commit `.env` file to Git!**

Always use `.env.example` as a template.

### Git Configuration

```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "*.log" >> .gitignore
echo "__pycache__/" >> .gitignore
```

### Security Best Practices

1. **Email Credentials**
   - Use app passwords, not account passwords
   - Never hardcode credentials
   - Use environment variables only
   - Rotate credentials regularly

2. **Database**
   - Use strong passwords
   - Enable MongoDB authentication
   - Regular backups
   - Encryption at rest

3. **Flask**
   - Generate strong secret key: `python -c "import secrets; print(secrets.token_hex(32))"`
   - HTTPS in production
   - CSRF protection enabled
   - Input validation on all forms

---

## Support & Resources

### Documentation
- [VEHICLES_SETUP.md](VEHICLES_SETUP.md) - Complete vehicle system guide
- [EMAIL_SETUP.md](EMAIL_SETUP.md) - Complete email system guide
- [README.md](README.md) - Project overview

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-Mail Documentation](https://pythonhosted.org/Flask-Mail/)
- [MongoDB Documentation](https://docs.mongodb.com/)

### Common Issues
- Check [EMAIL_SETUP.md](EMAIL_SETUP.md) "Troubleshooting" section
- Check [VEHICLES_SETUP.md](VEHICLES_SETUP.md) "Troubleshooting" section
- Review error logs in terminal

---

## Getting Help

If you encounter issues:

1. **Check Logs**
   ```bash
   # View Flask server output
   # Look for error messages
   ```

2. **Enable Debug Mode**
   ```python
   app.run(debug=True)
   ```

3. **Test Components Separately**
   ```python
   # Test email in Python console
   # Test database in Python console
   # Test Flask routes manually
   ```

4. **Consult Documentation**
   - Read [EMAIL_SETUP.md](EMAIL_SETUP.md)
   - Read [VEHICLES_SETUP.md](VEHICLES_SETUP.md)
   - Check Flask/Flask-Mail official docs

---

## Success Indicators ✅

You'll know everything is working when:

1. ✅ Registration page sends welcome email
2. ✅ Vehicles page displays available cars
3. ✅ Booking creates confirmation email
4. ✅ Dashboard shows vehicle link
5. ✅ All emails arrive in inbox within 30 seconds
6. ✅ Email templates render with proper styling
7. ✅ Booking dates save to database
8. ✅ Mobile design looks good on phones

---

**You're all set! 🎉**

Enjoy your TravelGo platform with complete email notifications and vehicle rental system!

**Last Updated:** January 2024
**Version:** 1.0.0
