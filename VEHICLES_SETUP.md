# 🚗 Vehicle Rental System - TravelGo

## Overview

The TravelGo Vehicle Rental System provides a complete car rental management solution integrated seamlessly with the travel booking platform. Users can search for vehicles, view detailed information, and complete bookings with automated email confirmations.

---

## Features

### ✨ Core Features

1. **Vehicle Search & Browse**
   - Search by location, dates, and vehicle type
   - Filter by category (Economy, Premium, SUV, Luxury)
   - Real-time availability check
   - Instant pricing display

2. **Detailed Vehicle Information**
   - Complete vehicle specifications
   - Features and amenities list
   - Insurance and cancellation policies
   - Multiple pickup locations
   - Customer reviews and ratings

3. **Easy Booking Flow**
   - One-click vehicle selection
   - Quick booking modal
   - Confirmation page with booking details
   - Automatic email notifications

4. **Email Integration**
   - Welcome emails on registration
   - Booking confirmation emails
   - Special offer promotions
   - Professional HTML templates with company branding

---

## File Structure

```
templates/
├── vehicles.html              # Main vehicle search and listing page
└── vehicle_details.html       # Detailed vehicle information page

static/
└── css/
    └── style.css             # (Already contains vehicle styling)

app.py
├── /vehicles route           # Vehicle search (GET/POST)
├── /vehicle-details route    # Vehicle detail view (GET)
├── /book-vehicle route       # Booking processing (POST)
└── Email functions           # send_booking_confirmation_email()

database/
└── vehicles_collection       # MongoDB collection for vehicle data

requirements.txt
└── Flask-Mail==0.9.1        # Email functionality
```

---

## Routes & API

### 1. Vehicle Search (`/vehicles`)
**Method:** GET, POST
**Description:** Display available vehicles with search filters

**GET Response:**
- Empty vehicle list on initial load
- Renders `vehicles.html`

**POST Request Parameters:**
```python
{
    "location": "New York",          # Pickup location
    "pickup_date": "2024-01-15",     # ISO date format
    "return_date": "2024-01-20",     # ISO date format
    "vehicle_type": "economy"         # economy|premium|suv|luxury
}
```

**POST Response:**
- Filtered vehicle list based on search criteria
- Renders `vehicles.html` with vehicles

**Sample Response Data:**
```python
vehicles = [
    {
        "id": "uuid",
        "name": "Toyota Corolla",
        "type": "Economy",
        "price": "$35",
        "image": "🚗",
        "transmission": "Automatic",
        "passengers": "5",
        "luggage": "2 bags",
        "fuel": "Petrol",
        "rating": "4.7",
        "mileage": "Unlimited"
    }
]
```

---

### 2. Vehicle Details (`/vehicle-details/<vehicle_id>`)
**Method:** GET
**Description:** Display comprehensive information about a specific vehicle

**Response Fields:**
```python
{
    "id": "vehicle_id",
    "name": "Toyota Corolla",
    "type": "Economy",
    "price_per_day": "$35",
    "image": "🚗",
    "transmission": "Automatic",
    "passengers": "5",
    "luggage": "2 bags",
    "fuel": "Petrol",
    "rating": "4.7",
    "mileage": "Unlimited",
    "description": "Perfect for budget travelers...",
    "features": [
        "Air Conditioning",
        "Power Steering",
        "ABS Brakes",
        "Bluetooth",
        "USB Charger",
        "Cruise Control"
    ],
    "insurance": "Full coverage",
    "cancellation": "Free cancellation up to 24 hours",
    "pickup_locations": ["Airport", "City Center", "Train Station"],
    "reviews": [
        {
            "user": "John D.",
            "rating": "5",
            "text": "Great car for the price..."
        }
    ]
}
```

---

### 3. Book Vehicle (`/book-vehicle`)
**Method:** POST
**Description:** Process vehicle booking and send confirmation email

**Request Parameters:**
```python
{
    "vehicle_name": "Toyota Corolla",
    "pickup_date": "2024-01-15",
    "return_date": "2024-01-20",
    "location": "New York"
}
```

**Database Insertion:**
```python
vehicle_booking = {
    "booking_id": uuid,
    "user": "user@email.com",
    "type": "vehicle",
    "vehicle_name": "Toyota Corolla",
    "pickup_date": "2024-01-15",
    "return_date": "2024-01-20",
    "location": "New York",
    "status": "confirmed",
    "created_at": datetime.now()
}
```

**Actions Performed:**
1. Generate unique booking ID
2. Store booking in database
3. Send confirmation email to user
4. Redirect to booking confirmation page

---

## Email System Integration

### Email Configuration

Set the following environment variables in your `.env` file:

```bash
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@travelgo.com
```

### Email Functions

#### 1. send_booking_confirmation_email()
**Triggered:** When vehicle booking is completed
**Recipient:** Customer email

**Template Variables:**
- `user_email`: Customer's email address
- `user_name`: Customer's full name
- `booking`: Booking dictionary with details

**Email Content:**
- Vehicle name and rental period
- Pickup and return locations
- Daily rate and total cost
- Cancellation policy
- Customer support contact

**HTML Features:**
- TravelGo brand colors (Cyan #00d4ff, Purple #7b2ff7)
- Professional layout with gradients
- Mobile-responsive design
- Clear call-to-action buttons

---

#### 2. send_special_offer_email()
**Triggered:** Promotional campaigns
**Usage:** For marketing special vehicle deals

**Template Variables:**
- `email`: Recipient email
- `name`: Recipient name
- `offer_title`: Promotion title
- `offer_description`: Promotion details
- `discount_percentage`: Discount amount

**Email Content:**
- Eye-catching offer banner
- Discount percentage display
- Limited-time urgency messaging
- Vehicle options
- Direct booking link

---

#### 3. send_welcome_email()
**Triggered:** On user registration
**Recipient:** New user email

**Template Variables:**
- `email`: New user's email
- `name`: User's full name

**Email Content:**
- Welcome greeting
- Platform features overview
- Special welcome bonus offer
- Quick start guide
- FAQ links

---

## Database Schema

### Vehicles Collection
```javascript
{
    _id: ObjectId,
    name: String,
    type: String,  // Economy, Premium, SUV, Luxury
    price_per_day: Decimal,
    make: String,
    model: String,
    year: Number,
    transmission: String,  // Automatic, Manual
    fuel_type: String,     // Petrol, Diesel, Hybrid
    passengers: Number,
    luggage_capacity: String,
    features: [String],
    rating: Number,  // 1-5 stars
    reviews_count: Number,
    insurance_options: [String],
    cancellation_policy: String,
    pickup_locations: [String],
    available_dates: {
        start: Date,
        end: Date
    },
    image_url: String,
    description: String,
    created_at: Date,
    updated_at: Date
}
```

### Bookings Collection (Vehicle)
```javascript
{
    _id: ObjectId,
    booking_id: String,  // UUID
    user: String,        // User email
    type: "vehicle",
    vehicle_name: String,
    pickup_date: Date,
    return_date: Date,
    location: String,
    status: String,      // confirmed, pending, cancelled
    created_at: Date,
    price_per_day: Decimal,
    total_price: Decimal,
    insurance_selected: String,
    driver_info: {
        name: String,
        license_number: String,
        phone: String
    }
}
```

---

## User Flow

### Vehicle Rental Process

```
1. User logs in to dashboard
2. Clicks "🚗 Rent Vehicles" or navigation link
3. Searches for vehicles:
   - Enters pickup location
   - Selects pickup date
   - Selects return date
   - Chooses vehicle type
4. Browses available vehicles:
   - Views vehicle cards with key specs
   - Sees price per day
   - Views rating and reviews
5. Selects a vehicle:
   - Clicks "View Details" for more info, OR
   - Clicks "Book Now" to start booking
6. Completes booking:
   - Booking modal appears
   - Confirms location and dates
   - Submits booking form
7. Booking confirmation:
   - Redirected to confirmation page
   - Booking details displayed
   - Confirmation email sent automatically
```

---

## Customization Guide

### Adding New Vehicle Types

Edit `/vehicles` route in `app.py`:

```python
vehicles_list = [
    {
        "id": str(uuid.uuid4()),
        "name": "Tesla Model 3",
        "type": "Electric",  # New type
        "price": "$55",
        "image": "🔌",
        "transmission": "Automatic",
        "passengers": "5",
        "luggage": "2 bags",
        "fuel": "Electric (300 miles range)",
        "rating": "4.9",
        "mileage": "Unlimited"
    }
]
```

### Modifying Email Templates

Edit `send_booking_confirmation_email()` in `app.py`:

```python
html_body = """
<html>
<body style="font-family: Poppins; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);">
    <!-- Customize your HTML email template here -->
    <h1 style="color: #00d4ff;">Booking Confirmation</h1>
    <!-- Add your custom styling and content -->
</body>
</html>
"""
```

### Changing Colors

Update the color scheme in `vehicles.html` and `vehicle_details.html`:

```css
/* Change TravelGo colors */
--primary-color: #00d4ff;    /* Cyan */
--secondary-color: #7b2ff7;  /* Purple */
--accent-color: #ff006e;     /* Pink */
--gold-color: #ffbe0b;       /* Gold */
```

---

## Testing

### Manual Testing Checklist

#### Search Functionality
- [ ] Search works with all filter combinations
- [ ] Date validation (return date > pickup date)
- [ ] Vehicle cards render correctly
- [ ] Sorting and filtering work

#### Booking Flow
- [ ] "Book Now" button opens modal
- [ ] Modal auto-fills vehicle name
- [ ] Date inputs have min date validation
- [ ] Booking saves to database
- [ ] Confirmation page displays booking details

#### Email Notifications
- [ ] Welcome email sent on registration
- [ ] Booking confirmation email sent after booking
- [ ] Email contains correct booking details
- [ ] Email templates render properly
- [ ] Images and styling display correctly

#### User Experience
- [ ] Mobile responsive design
- [ ] Navigation links work
- [ ] Forms validate input
- [ ] Error messages clear
- [ ] Loading states smooth

### Test Data Setup

Add sample vehicles to MongoDB:

```python
# Run in Python shell
from database.db import db

vehicles_data = [
    {
        "name": "Toyota Corolla",
        "type": "Economy",
        "price_per_day": 35,
        # ... other fields
    },
    # ... more vehicles
]

db["vehicles"].insert_many(vehicles_data)
```

---

## Integration with Existing Features

### Dashboard Integration
- ✅ Vehicle link added to navigation
- ✅ Vehicle card added to features grid
- ✅ Accessible from dashboard

### Booking System Integration
- ✅ Vehicle bookings stored in bookings collection
- ✅ Booking confirmation page works with vehicle bookings
- ✅ Booking status tracking

### Email System Integration
- ✅ Flask-Mail configured
- ✅ Booking confirmation emails sent
- ✅ Welcome emails on registration
- ✅ Special offer emails available

### Profile & History
- Vehicle bookings visible in booking history
- Rentals tracked in user profile
- Past vehicles in recommendation engine

---

## Troubleshooting

### Email Not Sending

**Problem:** Emails not being sent

**Solutions:**
1. Verify environment variables in `.env`
2. Check Gmail app password (not account password)
3. Enable "Less secure app access" if using Gmail
4. Check email logs: `app.logger.error(str(e))`

Example:
```python
# Add to email functions
try:
    mail.send(msg)
except Exception as e:
    app.logger.error(f"Email failed: {str(e)}")
```

### Vehicles Not Appearing

**Problem:** No vehicles showing in search results

**Solutions:**
1. Check database connection
2. Verify sample data inserted
3. Check filter logic in Python
4. Verify Jinja2 template rendering

### Booking Not Saving

**Problem:** Bookings not stored in database

**Solutions:**
1. Check MongoDB connection
2. Verify bookings collection exists
3. Check user session data
4. Enable database logging

---

## Performance Optimization

### Database Indexing

```python
# In database/db.py
db["vehicles"].create_index([("type", 1)])
db["vehicles"].create_index([("price_per_day", 1)])
db["bookings"].create_index([("user", 1), ("created_at", -1)])
```

### Caching

For frequently accessed vehicle lists:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_vehicles_by_type(vehicle_type):
    return list(vehicles_collection.find({"type": vehicle_type}))
```

### Pagination

Implement for large vehicle lists:

```python
@app.route('/vehicles/page/<int:page>')
def vehicles_paginated(page):
    items_per_page = 12
    skip = (page - 1) * items_per_page
    vehicles = list(vehicles_collection.find().skip(skip).limit(items_per_page))
    return render_template("vehicles.html", vehicles=vehicles, page=page)
```

---

## Security Considerations

### Input Validation

```python
from datetime import datetime

def validate_booking_dates(pickup, return_date):
    pickup_dt = datetime.fromisoformat(pickup)
    return_dt = datetime.fromisoformat(return_date)
    
    if return_dt <= pickup_dt:
        raise ValueError("Return date must be after pickup date")
    if pickup_dt < datetime.now():
        raise ValueError("Pickup date cannot be in the past")
```

### SQL Injection Protection
- Using DynamoDB access patterns (boto3) - ✅ Safe
- No raw string concatenation in queries - ✅ Safe

### Authentication
- Check session before allowing bookings
- Verified in `/vehicles` and `/book-vehicle` routes
- Email confirmation adds verification layer

---

## Future Enhancements

### Planned Features
1. **GPS Tracking** - Real-time vehicle location
2. **Insurance Add-ons** - Optional coverage plans
3. **Driver Requirements** - License upload/verification
4. **Payment Gateway** - Stripe/PayPal integration
5. **Loyalty Program** - Points and rewards
6. **Review System** - User ratings and comments
7. **Damage Reports** - Pre/post rental photo documentation
8. **Pickup Scheduling** - Appointment booking system
9. **Fleet Management** - Admin vehicle management dashboard
10. **Analytics** - Occupancy rates and revenue tracking

---

## Deployment Checklist

- [ ] Environment variables configured on server
- [ ] Email credentials verified
- [ ] MongoDB backup configured
- [ ] HTTPS enabled
- [ ] Security headers added
- [ ] Rate limiting configured
- [ ] Error logging enabled
- [ ] Database indexes created
- [ ] Admin panel set up for vehicle management
- [ ] Documentation updated

---

## Support & FAQ

**Q: How do I add more vehicles?**
A: Add vehicles to the sample data in the `/vehicles` route, or use MongoDB directly.

**Q: Can I customize the email template?**
A: Yes, edit the HTML in `send_booking_confirmation_email()` function in `app.py`.

**Q: How do I enable payment processing?**
A: Integrate Stripe/PayPal in the `/book-vehicle` route before saving the booking.

**Q: Can users modify bookings?**
A: Currently not implemented. Add a `/update-vehicle-booking` route for this feature.

**Q: How do I track email delivery?**
A: Implement webhook logging with your email service provider.

---

## License & Credits

TravelGo Vehicle Rental System - Part of TravelGo Travel Booking Platform

Built with:
- Flask 2.3.2
- MongoDB 4.4.0
- Flask-Mail 0.9.1
- Python 3.8+

---

## Contact & Feedback

For questions, improvements, or support regarding the vehicle rental system, contact the development team.

Last Updated: January 2024
Version: 1.0.0
