# 📧 Email Notification System - TravelGo

## Overview

The TravelGo Email Notification System provides automated, beautifully designed email communications for user engagement, booking confirmations, and marketing campaigns. All emails are HTML-based with inline CSS styling matching the TravelGo brand.

---

## Quick Start

### 1. Configure Environment Variables

Create a `.env` file in your project root:

```bash
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@travelgo.com
```

### 2. Install Dependencies

```bash
pip install flask-mail==0.9.1 python-dateutil==2.8.2
```

### 3. Update app.py Configuration

```python
from flask_mail import Mail

# Email Configuration (from environment variables)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@travelgo.com')

mail = Mail(app)
```

---

## Email Functions

### 1. Send Booking Confirmation Email

**Function Signature:**
```python
def send_booking_confirmation_email(email, name, booking):
    """
    Send booking confirmation email to user
    
    Args:
        email (str): User's email address
        name (str): User's full name
        booking (dict): Booking details dictionary
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
```

**Triggered By:**
- Vehicle booking completion
- Hotel booking completion
- Flight booking completion
- Any booking type in `/book-vehicle`, `/book-hotel`, etc.

**Email Content Includes:**
- Booking confirmation number
- Reservation details
- Dates and locations
- Cost breakdown
- Cancellation policy
- Customer support contact

**Example Usage:**
```python
@app.route('/book-vehicle', methods=['POST'])
def book_vehicle():
    # ... booking logic ...
    
    # Send confirmation email
    user = users.find_one({"email": session['user']})
    if user:
        send_booking_confirmation_email(
            session['user'],
            user.get('name', 'Traveler'),
            vehicle_booking
        )
    
    return redirect(f'/booking-confirmation/{booking_id}')
```

**Email Template Preview:**
```
┌─────────────────────────────────────────┐
│  TRAVELGO - Booking Confirmation        │
├─────────────────────────────────────────┤
│                                         │
│  Dear [Name],                          │
│                                         │
│  Your booking has been confirmed!      │
│                                         │
│  📋 Confirmation #: abc123             │
│  🏨 Vehicle: Toyota Corolla            │
│  📅 Pickup: Jan 15, 2024               │
│  📅 Return: Jan 20, 2024               │
│  💰 Total: $175.00                     │
│                                         │
│  [View Booking Details]                │
│                                         │
│  Need help? Contact support@travelgo.com
│                                         │
└─────────────────────────────────────────┘
```

---

### 2. Send Special Offer Email

**Function Signature:**
```python
def send_special_offer_email(email, name, offer_title, offer_description, discount_percentage):
    """
    Send promotional email with special offers
    
    Args:
        email (str): Recipient email address
        name (str): Recipient's name
        offer_title (str): Title of the offer
        offer_description (str): Detailed description
        discount_percentage (int): Discount amount
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
```

**Triggered By:**
- Marketing campaigns
- Limited-time promotions
- Seasonal sales
- Loyalty rewards
- Flash deals

**Email Content Includes:**
- Offer headline with discount percentage
- Eye-catching banner
- Offer description
- Terms and conditions
- Call-to-action button
- Expiration date

**Example Usage:**
```python
# Send promotion to specific user
send_special_offer_email(
    email="john@example.com",
    name="John Doe",
    offer_title="Summer Vacation Special",
    offer_description="Get 30% off on vehicle rentals this summer!",
    discount_percentage=30
)
```

**Email Template Preview:**
```
┌─────────────────────────────────────────┐
│  TRAVELGO - Special Offer               │
├─────────────────────────────────────────┤
│                                         │
│  🎉 LIMITED TIME OFFER! 🎉             │
│                                         │
│  Hi John,                               │
│                                         │
│  Summer Vacation Special                │
│  Get 30% off on vehicle rentals!       │
│                                         │
│  Your exclusive discount code:         │
│  SUMMER30                               │
│                                         │
│  [Claim Your Discount]                 │
│                                         │
│  Offer expires: Dec 31, 2024           │
│                                         │
└─────────────────────────────────────────┘
```

---

### 3. Send Welcome Email

**Function Signature:**
```python
def send_welcome_email(email, name):
    """
    Send welcome email to new users
    
    Args:
        email (str): New user's email address
        name (str): New user's full name
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
```

**Triggered By:**
- User registration/sign-up
- New account creation
- First-time login (optional)

**Email Content Includes:**
- Warm welcome greeting
- Platform introduction
- Key features overview
- Special welcome bonus offer
- Quick start guide
- FAQ links

**Example Usage:**
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # ... registration logic ...
        
        # Send welcome email
        send_welcome_email(email, name)
        
        return redirect('/login')
    
    return render_template('register.html')
```

**Email Template Preview:**
```
┌─────────────────────────────────────────┐
│  TRAVELGO - Welcome!                    │
├─────────────────────────────────────────┤
│                                         │
│  Welcome to TravelGo, John!             │
│                                         │
│  We're excited to have you on board!   │
│                                         │
│  🎁 Welcome Bonus: 20% off your        │
│     first booking!                      │
│                                         │
│  What you can do:                       │
│  • Search destinations                  │
│  • Book hotels and flights              │
│  • Rent vehicles                        │
│  • Read travel tips from experts        │
│                                         │
│  [Get Started Now]                      │
│                                         │
│  Questions? Check our FAQ               │
│                                         │
└─────────────────────────────────────────┘
```

---

## Email Configuration Details

### Gmail SMTP (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to Google Account Security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your device)
   - Google will generate a 16-character password

3. **Configure Environment Variables**
   ```bash
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx  # 16-char app password
   MAIL_DEFAULT_SENDER=noreply@travelgo.com
   ```

### Other SMTP Servers

**SendGrid:**
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.XXXXXXXXXXXXXXXXXXXX
```

**Mailgun:**
```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=postmaster@travelgo.mailgun.org
MAIL_PASSWORD=your-mailgun-password
```

**AWS SES:**
```bash
MAIL_SERVER=email-smtp.us-east-1.amazonaws.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-ses-username
MAIL_PASSWORD=your-ses-password
```

---

## HTML Email Templates

### Base Email Structure

All TravelGo emails follow this structure:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Poppins', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            margin: 0;
            padding: 20px;
        }
        
        .email-container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(26, 26, 46, 0.95);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
        }
        
        .header {
            background: linear-gradient(135deg, #00d4ff, #7b2ff7);
            color: #000;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .content {
            color: #a0a0a0;
            line-height: 1.6;
        }
        
        .cta-button {
            background: linear-gradient(135deg, #00d4ff, #7b2ff7);
            color: #000;
            padding: 12px 30px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            display: inline-block;
            margin: 20px 0;
        }
        
        .footer {
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            margin-top: 30px;
            border-top: 1px solid rgba(0, 212, 255, 0.2);
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="header">
            <h1>TravelGo</h1>
        </div>
        
        <!-- Content -->
        <div class="content">
            <h2>Your Message Here</h2>
            <p>Email body content...</p>
        </div>
        
        <!-- CTA Button -->
        <a href="https://travelgo.com/booking/{{ id }}" class="cta-button">View Details</a>
        
        <!-- Footer -->
        <div class="footer">
            <p>&copy; 2024 TravelGo. All rights reserved.</p>
            <p>Contact: support@travelgo.com</p>
        </div>
    </div>
</body>
</html>
```

---

## Customizing Email Templates

### Edit Booking Confirmation Email

In `app.py`, find `send_booking_confirmation_email()`:

```python
def send_booking_confirmation_email(email, name, booking):
    msg = Message(
        subject=f"Booking Confirmation - {booking_id}",
        recipients=[email]
    )
    
    # Customize this HTML
    msg.html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Poppins; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #fff;">
        <div style="max-width: 600px; margin: 0 auto; background: rgba(26, 26, 46, 0.95); padding: 30px; border-radius: 15px; border: 2px solid rgba(0, 212, 255, 0.3);">
            
            <h1 style="background: linear-gradient(135deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Booking Confirmation
            </h1>
            
            <p>Dear {name},</p>
            
            <p>Your booking has been confirmed! Here are your details:</p>
            
            <div style="background: rgba(0, 212, 255, 0.1); padding: 20px; border-radius: 10px; border-left: 3px solid #00d4ff;">
                <p><strong>Confirmation ID:</strong> {booking_id}</p>
                <p><strong>Vehicle:</strong> {booking.get('vehicle_name', 'N/A')}</p>
                <p><strong>Pickup Date:</strong> {booking.get('pickup_date', 'N/A')}</p>
                <p><strong>Return Date:</strong> {booking.get('return_date', 'N/A')}</p>
                <p><strong>Location:</strong> {booking.get('location', 'N/A')}</p>
            </div>
            
            <p style="margin-top: 20px;">Your confirmation code has been saved. You'll need this for pickup.</p>
            
            <a href="https://travelgo.com/booking/{booking_id}" style="background: linear-gradient(135deg, #00d4ff, #7b2ff7); color: #000; padding: 12px 30px; border-radius: 5px; text-decoration: none; font-weight: bold; display: inline-block; margin: 20px 0;">View Full Details</a>
            
            <p style="color: #a0a0a0; font-size: 0.9rem; margin-top: 30px;">
                If you have any questions, please contact our support team at support@travelgo.com
            </p>
            
        </div>
    </body>
    </html>
    """
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Email error: {str(e)}")
        return False
```

---

## Email Triggers & Automation

### Current Triggers

| Event | Email Type | Function | Trigger Point |
|-------|-----------|----------|----------------|
| User Registration | Welcome | `send_welcome_email()` | `/register` route |
| Hotel Booking | Confirmation | `send_booking_confirmation_email()` | `/book-hotel` route |
| Flight Booking | Confirmation | `send_booking_confirmation_email()` | `/book-flight` route |
| Vehicle Booking | Confirmation | `send_booking_confirmation_email()` | `/book-vehicle` route |

### Adding New Triggers

```python
# Example: Send email on booking cancellation
@app.route('/cancel-booking/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    # ... cancellation logic ...
    
    # Send cancellation email
    user = users.find_one({"email": session['user']})
    send_cancellation_email(session['user'], user.get('name'))
    
    return redirect('/bookings')

def send_cancellation_email(email, name):
    msg = Message(
        subject="Booking Cancelled",
        recipients=[email]
    )
    msg.html = f"""
    <html>
    <body>
        <h1>Booking Cancelled</h1>
        <p>Hi {name},</p>
        <p>Your booking has been successfully cancelled.</p>
    </body>
    </html>
    """
    mail.send(msg)
```

---

## Testing Email System

### 1. Test Configuration

```python
# In Python shell or test script
from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure email
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Test send
with app.app_context():
    msg = Message(
        subject="Test Email",
        recipients=["your-email@example.com"]
    )
    msg.body = "This is a test email"
    mail.send(msg)
    print("Email sent successfully!")
```

### 2. Test Functions Directly

```python
from app import app, send_welcome_email, send_booking_confirmation_email

with app.app_context():
    # Test welcome email
    send_welcome_email("test@example.com", "Test User")
    print("Welcome email sent!")
    
    # Test booking confirmation
    booking = {
        "booking_id": "TEST123",
        "vehicle_name": "Toyota Corolla",
        "pickup_date": "2024-01-15",
        "return_date": "2024-01-20",
        "location": "New York"
    }
    send_booking_confirmation_email("test@example.com", "Test User", booking)
    print("Booking email sent!")
```

### 3. Check Email Logs

```python
# Add logging to email functions
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def send_welcome_email(email, name):
    try:
        msg = Message(...)
        mail.send(msg)
        logger.info(f"Welcome email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")
```

---

## Email Best Practices

### ✅ Do's

- **Use HTML templates** for professional formatting
- **Inline CSS** for email client compatibility
- **Test across clients** (Gmail, Outlook, Apple Mail, etc.)
- **Make emails responsive** with media queries
- **Include unsubscribe links** for compliance
- **Personalize with user data** (name, booking details)
- **Use clear call-to-action buttons** with good contrast
- **Keep emails short** (under 600px width)
- **Always include contact info** for support
- **Monitor delivery rates** and adjust configuration

### ❌ Don'ts

- **Don't use complex images** - stick to simple graphics
- **Don't embed files** - link to files instead
- **Don't use external stylesheets** - use inline CSS only
- **Don't use JavaScript** - email clients don't support it
- **Don't send too many emails** - respect user preferences
- **Don't hardcode credentials** - use environment variables
- **Don't forget alt text** for images
- **Don't use long URLs** - use URL shorteners
- **Don't forget to test** - test before deploying
- **Don't ignore bounce rates** - monitor delivery health

---

## Troubleshooting

### Email Not Sending

**Problem:** `SMTPAuthenticationError`

**Solution:**
1. Verify MAIL_USERNAME and MAIL_PASSWORD
2. For Gmail: Use app password, not account password
3. Check that 2-Factor Authentication is enabled
4. Verify MAIL_SERVER and MAIL_PORT are correct

```python
# Test credentials
import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'app-password')
    print("SMTP connection successful!")
except Exception as e:
    print(f"SMTP connection failed: {e}")
```

### Email Content Not Rendering

**Problem:** HTML not displaying properly

**Solution:**
1. Ensure all CSS is inline (no `<style>` tags in templates)
2. Test in email client simulators (Stripo, Email on Acid)
3. Avoid unsupported CSS (animations, custom fonts)
4. Use standard HTML attributes

### High Bounce Rate

**Problem:** Many emails not reaching recipients

**Solution:**
1. Verify all email addresses in database
2. Use email validation library
3. Monitor bounce lists
4. Implement remove-from-list functionality

```python
# Email validation
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Use before sending
if is_valid_email(user_email):
    send_welcome_email(user_email, user_name)
```

---

## Performance Optimization

### Background Email Sending

Send emails asynchronously to avoid blocking requests:

```python
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_booking_confirmation_email(email, name, booking):
    msg = Message(...)
    
    # Send in background thread
    Thread(target=send_async_email, args=(app, msg)).start()
    
    return True
```

### Batch Email Sending

Send multiple emails efficiently:

```python
def send_batch_offers(recipients, offer_title, discount):
    """Send offer emails to multiple users"""
    for email, name in recipients:
        Thread(target=send_async_email, args=(
            app,
            Message(
                subject="Special Offer!",
                recipients=[email],
                html=f"<h1>{offer_title}</h1><p>Get {discount}% off!"
            )
        )).start()
```

### Email Queue System

For production, consider using Celery:

```python
# pip install celery
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379')

@celery.task
def send_email_async(email, subject, html):
    msg = Message(subject=subject, recipients=[email])
    msg.html = html
    mail.send(msg)

# Usage
send_email_async.delay(user_email, "Confirmation", html_content)
```

---

## Compliance & Legal

### GDPR Compliance

- Implement opt-in for marketing emails
- Provide easy unsubscribe mechanism
- Honor user preferences
- Keep minimal data retention

### CAN-SPAM Compliance

- Include physical address in emails
- Provide clear unsubscribe option
- Honor unsubscribe requests within 10 days
- Accurate subject lines

```python
# Add unsubscribe to footer
unsubscribe_link = "https://travelgo.com/unsubscribe?email=" + urllib.parse.quote(email)

footer = f"""
<div style="text-align: center; color: #666; font-size: 0.8rem; margin-top: 30px;">
    <p>© 2024 TravelGo, Inc.</p>
    <p>123 Travel Street, Adventure City, AC 12345</p>
    <p><a href="{unsubscribe_link}">Unsubscribe from marketing emails</a></p>
</div>
"""
```

---

## Analytics & Monitoring

### Track Email Metrics

```python
from datetime import datetime

# Log email sends
def log_email(email, email_type, status):
    email_log = {
        "recipient": email,
        "type": email_type,  # welcome, booking, offer, etc.
        "status": status,    # sent, failed
        "timestamp": datetime.now()
    }
    db["email_logs"].insert_one(email_log)

# Usage
try:
    send_welcome_email(email, name)
    log_email(email, "welcome", "sent")
except:
    log_email(email, "welcome", "failed")

# Analytics
def get_email_stats():
    return db["email_logs"].aggregate([
        {"$group": {
            "_id": "$type",
            "sent": {"$sum": {"$cond": [{"$eq": ["$status", "sent"]}, 1, 0]}},
            "failed": {"$sum": {"$cond": [{"$eq": ["$status", "failed"]}, 1, 0]}}
        }}
    ])
```

---

## Complete Implementation Checklist

- [ ] Install Flask-Mail: `pip install flask-mail==0.9.1`
- [ ] Create `.env` file with SMTP credentials
- [ ] Update `app.py` with email configuration
- [ ] Implement email functions
- [ ] Add Flask-Mail trigger to registration route
- [ ] Test email functionality
- [ ] Customize email templates with company branding
- [ ] Set up email logging
- [ ] Configure background email sending
- [ ] Add bounce handling
- [ ] Implement unsubscribe mechanism
- [ ] Test across email clients
- [ ] Monitor delivery rates
- [ ] Document email system
- [ ] Deploy to production

---

## Support

For email system support, issues, or improvements, contact the development team.

**Last Updated:** January 2024
**Version:** 1.0.0
**Status:** Production Ready ✅
