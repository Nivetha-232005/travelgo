from flask import Flask, render_template, request, redirect, session, jsonify
from config import users, bookings, plans
from database.db import users_collection, bookings_collection, plans_collection
import os
import uuid
from datetime import datetime
from flask_mail import Mail, Message

try:
    from database.dynamodb_seed import seed_plans_to_dynamodb
except Exception:
    seed_plans_to_dynamodb = None

app = Flask(__name__)
app.secret_key = "travelgo_secret_v2"


def render_error_page(error_code, error_title, error_message, status_code=None):
    code = status_code if status_code is not None else error_code
    return render_template(
        "error_page.html",
        error_code=error_code,
        error_title=error_title,
        error_message=error_message,
    ), code


@app.route('/error/invalid-login')
def invalid_login_error():
    return render_error_page(
        401,
        "Invalid Login",
        "Email or password is incorrect. Please check your credentials and try again.",
        401,
    )


@app.route('/error/failed-fetch')
def failed_fetch_error():
    return render_error_page(
        503,
        "Failed To Fetch",
        "Unable to reach the server. Please check your network or try again in a moment.",
        503,
    )


@app.route('/error/database')
def database_error_page():
    return render_error_page(
        500,
        "Database Connection Error",
        "TravelGo could not connect to the database. Please verify database settings and try again.",
        500,
    )

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@travelgo.com'

mail = Mail(app)


def format_inr(value):
    """Format numbers or USD-like strings as Indian Rupees."""
    usd_to_inr = 83

    if value is None:
        return "₹0"

    if isinstance(value, (int, float)):
        return f"₹{int(round(value)):,}"

    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned.startswith("$"):
            numeric = ''.join(ch for ch in cleaned if ch.isdigit() or ch == '.')
            if numeric:
                return f"₹{int(round(float(numeric) * usd_to_inr)):,}"
        if cleaned.startswith("₹"):
            return cleaned
        if cleaned.isdigit():
            return f"₹{int(cleaned):,}"

    return str(value)


def get_plan_image_url(plan_name):
    """Return a representative image URL for each plan."""
    image_map = {
        "Parisian Romance": "https://images.unsplash.com/photo-1431274172761-fca41d930114?auto=format&fit=crop&w=1200&q=80",
        "Tropical Bali Escape": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
        "Tokyo Adventure": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1200&q=80",
        "Dubai Luxury Experience": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
        "Swiss Alps Retreat": "https://images.unsplash.com/photo-1508261305437-4f24efc34d50?auto=format&fit=crop&w=1200&q=80",
        "Barcelona Beach & Culture": "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?auto=format&fit=crop&w=1200&q=80",
        "Budget Bangkok Explorer": "https://images.unsplash.com/photo-1563492065599-3520f775eeed?auto=format&fit=crop&w=1200&q=80",
        "Maldives Paradise": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80",
        "New York City Buzz": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?auto=format&fit=crop&w=1200&q=80",
        "Himalayan Trek": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
        "Royal Rajasthan Road Trip": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1200&q=80",
        "India Rail Explorer": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=1200&q=80"
    }
    return image_map.get(plan_name, "https://images.unsplash.com/photo-1488085061387-422e29b40080?auto=format&fit=crop&w=1200&q=80")


def enrich_plan_images(plan_docs):
    for plan in plan_docs:
        if not plan.get('image_url'):
            plan['image_url'] = get_plan_image_url(plan.get('name', ''))
    return plan_docs


app.jinja_env.filters['inr'] = format_inr

# Initialize collections
hotels_collection = None
flights_collection = None
reviews_collection = None
wishlist_collection = None
vehicles_collection = None

try:
    from database.db import db
    hotels_collection = db["hotels"]
    flights_collection = db["flights"]
    reviews_collection = db["reviews"]
    wishlist_collection = db["wishlist"]
    vehicles_collection = db["vehicles"]
except:
    pass


# Seed travel plans into database on startup
def seed_plans():
    if plans.count_documents({}) == 0:
        plans.insert_many([
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Parisian Romance",
                "destination": "Paris, France",
                "source": "Any City",
                "duration": "5 Days / 4 Nights",
                "price": 1200,
                "category": "culture",
                "budget": "premium",
                "max_travelers": 6,
                "rating": 4.9,
                "icon": "🗼",
                "image_url": "https://images.unsplash.com/photo-1431274172761-fca41d930114?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise", "Montmartre"],
                "includes": ["Hotel", "Breakfast", "City Tour", "Airport Transfer"],
                "image_emoji": "🇫🇷"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Tropical Bali Escape",
                "destination": "Bali, Indonesia",
                "source": "Any City",
                "duration": "7 Days / 6 Nights",
                "price": 950,
                "category": "beach",
                "budget": "moderate",
                "max_travelers": 8,
                "rating": 4.8,
                "icon": "🏝️",
                "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Ubud Terraces", "Tanah Lot Temple", "Kuta Beach", "Monkey Forest"],
                "includes": ["Resort Stay", "All Meals", "Spa Treatment", "Guided Tour"],
                "image_emoji": "🌴"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Tokyo Adventure",
                "destination": "Tokyo, Japan",
                "source": "Any City",
                "duration": "6 Days / 5 Nights",
                "price": 1500,
                "category": "culture",
                "budget": "premium",
                "max_travelers": 4,
                "rating": 4.7,
                "icon": "🎌",
                "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Shibuya Crossing", "Mt. Fuji Day Trip", "Akihabara", "Tsukiji Market"],
                "includes": ["Hotel", "Breakfast", "JR Rail Pass", "Airport Transfer"],
                "image_emoji": "🇯🇵"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Dubai Luxury Experience",
                "destination": "Dubai, UAE",
                "source": "Any City",
                "duration": "5 Days / 4 Nights",
                "price": 2200,
                "category": "adventure",
                "budget": "luxury",
                "max_travelers": 4,
                "rating": 4.9,
                "icon": "🌆",
                "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Burj Khalifa", "Desert Safari", "Dubai Mall", "Palm Jumeirah"],
                "includes": ["5-Star Hotel", "All Meals", "Desert Safari", "Yacht Tour"],
                "image_emoji": "🇦🇪"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Swiss Alps Retreat",
                "destination": "Interlaken, Switzerland",
                "source": "Any City",
                "duration": "4 Days / 3 Nights",
                "price": 1800,
                "category": "mountains",
                "budget": "premium",
                "max_travelers": 6,
                "rating": 4.8,
                "icon": "⛰️",
                "image_url": "https://images.unsplash.com/photo-1508261305437-4f24efc34d50?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Jungfraujoch", "Paragliding", "Lake Thun", "Grindelwald"],
                "includes": ["Chalet Stay", "Breakfast & Dinner", "Ski Pass", "Train Pass"],
                "image_emoji": "🇨🇭"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Barcelona Beach & Culture",
                "destination": "Barcelona, Spain",
                "source": "Any City",
                "duration": "5 Days / 4 Nights",
                "price": 780,
                "category": "beach",
                "budget": "moderate",
                "max_travelers": 8,
                "rating": 4.6,
                "icon": "🏖️",
                "image_url": "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Sagrada Familia", "La Rambla", "Park Güell", "Barceloneta Beach"],
                "includes": ["Hotel", "Breakfast", "City Pass", "Tapas Tour"],
                "image_emoji": "🇪🇸"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Budget Bangkok Explorer",
                "destination": "Bangkok, Thailand",
                "source": "Any City",
                "duration": "5 Days / 4 Nights",
                "price": 450,
                "category": "food",
                "budget": "budget",
                "max_travelers": 10,
                "rating": 4.5,
                "icon": "🛕",
                "image_url": "https://images.unsplash.com/photo-1563492065599-3520f775eeed?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Grand Palace", "Floating Markets", "Street Food Tour", "Wat Pho"],
                "includes": ["Hostel", "Breakfast", "Tuk-Tuk Tour", "Street Food Walk"],
                "image_emoji": "🇹🇭"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Maldives Paradise",
                "destination": "Maldives",
                "source": "Any City",
                "duration": "6 Days / 5 Nights",
                "price": 3200,
                "category": "beach",
                "budget": "luxury",
                "max_travelers": 2,
                "rating": 5.0,
                "icon": "🏝️",
                "image_url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Overwater Villa", "Snorkeling", "Sunset Cruise", "Underwater Restaurant"],
                "includes": ["Overwater Bungalow", "All-inclusive", "Water Sports", "Spa"],
                "image_emoji": "🇲🇻"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "New York City Buzz",
                "destination": "New York, USA",
                "source": "Any City",
                "duration": "4 Days / 3 Nights",
                "price": 1100,
                "category": "culture",
                "budget": "moderate",
                "max_travelers": 6,
                "rating": 4.7,
                "icon": "🗽",
                "image_url": "https://images.unsplash.com/photo-1485871981521-5b1fd3805eee?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Statue of Liberty", "Central Park", "Times Square", "Broadway Show"],
                "includes": ["Hotel", "Breakfast", "CityPASS", "Airport Shuttle"],
                "image_emoji": "🇺🇸"
            },
            {
                "plan_id": str(uuid.uuid4()),
                "name": "Himalayan Trek",
                "destination": "Nepal",
                "source": "Any City",
                "duration": "8 Days / 7 Nights",
                "price": 600,
                "category": "mountains",
                "budget": "budget",
                "max_travelers": 12,
                "rating": 4.6,
                "icon": "🏔️",
                "image_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
                "highlights": ["Annapurna Base Camp", "Pokhara", "Kathmandu Valley", "Sunrise at Poon Hill"],
                "includes": ["Lodge Stay", "All Meals on Trek", "Guide & Porter", "Permits"],
                "image_emoji": "🇳🇵"
            }
        ])
        print("✅ Travel plans seeded into database")


def ensure_transport_plans():
    transport_plans = [
        {
            "plan_id": str(uuid.uuid4()),
            "name": "Royal Rajasthan Road Trip",
            "destination": "Jaipur to Jaisalmer, India",
            "source": "Delhi",
            "duration": "6 Days / 5 Nights",
            "price": 42000,
            "category": "adventure",
            "budget": "moderate",
            "max_travelers": 5,
            "rating": 4.7,
            "icon": "🚗",
            "image_url": get_plan_image_url("Royal Rajasthan Road Trip"),
            "highlights": ["Jaipur Forts", "Pushkar", "Jodhpur Blue City", "Jaisalmer Dunes"],
            "includes": ["SUV Rental", "Hotel Stay", "Driver", "Fuel"],
            "image_emoji": "🇮🇳"
        },
        {
            "plan_id": str(uuid.uuid4()),
            "name": "India Rail Explorer",
            "destination": "Delhi, Agra, Varanasi, Kolkata",
            "source": "Delhi",
            "duration": "7 Days / 6 Nights",
            "price": 36000,
            "category": "culture",
            "budget": "budget",
            "max_travelers": 6,
            "rating": 4.6,
            "icon": "🚆",
            "image_url": get_plan_image_url("India Rail Explorer"),
            "highlights": ["Taj Mahal", "Ganga Aarti", "Howrah Bridge", "Local Cuisine"],
            "includes": ["Train Tickets", "Hotel", "Breakfast", "Guided Tours"],
            "image_emoji": "🇮🇳"
        }
    ]

    for plan in transport_plans:
        exists = plans.find_one({"name": plan["name"]})
        if not exists:
            plans.insert_one(plan)


def auto_seed_dynamodb_plans_on_startup():
    """Seed the same plans into DynamoDB whenever the app starts."""
    if seed_plans_to_dynamodb is None:
        print("⚠️ DynamoDB seed module not available. Skipping DynamoDB seed.")
        return

    table_name = os.getenv('DYNAMODB_PLANS_TABLE', 'plans')
    region_name = os.getenv('AWS_REGION', 'ap-south-1')
    endpoint_url = os.getenv('DYNAMODB_ENDPOINT_URL')
    force_seed = os.getenv('DYNAMODB_FORCE_SEED', 'false').lower() in {'1', 'true', 'yes', 'on'}
    auto_seed_enabled = os.getenv('DYNAMODB_AUTO_SEED', 'false').lower() in {'1', 'true', 'yes', 'on'}

    if not auto_seed_enabled and not endpoint_url:
        print('ℹ️ DynamoDB auto-seed skipped (set DYNAMODB_AUTO_SEED=true or DYNAMODB_ENDPOINT_URL).')
        return

    result = seed_plans_to_dynamodb(
        table_name=table_name,
        region_name=region_name,
        endpoint_url=endpoint_url,
        force=force_seed,
    )

    status = result.get('status')
    if status == 'success':
        print(
            f"✅ DynamoDB plans seed completed: inserted={result.get('inserted', 0)}, "
            f"skipped={result.get('skipped', 0)}, table={table_name}"
        )
    elif status == 'skipped':
        print(f"ℹ️ DynamoDB seed skipped ({result.get('reason', 'no reason')}) for table={table_name}")
    else:
        print(f"⚠️ DynamoDB seed failed: {result.get('error', 'Unknown error')}")

seed_plans()
ensure_transport_plans()
auto_seed_dynamodb_plans_on_startup()


# Email Notification Functions
def send_booking_confirmation_email(user_email, user_name, booking_details):
    """Send booking confirmation email"""
    try:
        subject = f"✈️ TravelGo Booking Confirmation - {booking_details.get('booking_id', 'N/A')}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background: linear-gradient(135deg, #0a0e27 0%, #1a1f4b 50%, #0f0c29 100%); color: #fff; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 30px; backdrop-filter: blur(10px);">
                    <h1 style="color: #00d4ff; text-align: center; margin-bottom: 30px;">✅ Booking Confirmed!</h1>
                    
                    <h2 style="color: #00d4ff; margin-top: 20px;">Booking Details</h2>
                    <div style="background: rgba(0, 212, 255, 0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
                        <p><strong>Booking ID:</strong> {booking_details.get('booking_id', 'N/A')}</p>
                        <p><strong>Type:</strong> {booking_details.get('type', 'Travel').title()}</p>
                        <p><strong>Booking Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
                        <p><strong>Status:</strong> <span style="color: #4caf50; font-weight: bold;">✓ CONFIRMED</span></p>
                    </div>
                    
                    <h2 style="color: #00d4ff; margin-top: 20px;">Trip Information</h2>
                    <div style="background: rgba(123, 47, 247, 0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
                        {f'<p><strong>Destination:</strong> {booking_details.get("destination", "N/A")}</p>' if 'destination' in booking_details else ''}
                        {f'<p><strong>Hotel:</strong> {booking_details.get("name", "N/A")}</p>' if 'name' in booking_details else ''}
                        {f'<p><strong>Check-in:</strong> {booking_details.get("check_in", "N/A")}</p>' if 'check_in' in booking_details else ''}
                        {f'<p><strong>Check-out:</strong> {booking_details.get("check_out", "N/A")}</p>' if 'check_out' in booking_details else ''}
                        {f'<p><strong>Travelers:</strong> {booking_details.get("travelers", "1")}</p>' if 'travelers' in booking_details else ''}
                    </div>
                    
                    <h2 style="color: #00d4ff; margin-top: 20px;">What's Next?</h2>
                    <ul style="color: rgba(255, 255, 255, 0.8);">
                        <li>Check your email for additional details</li>
                        <li>Download your confirmation PDF</li>
                        <li>Get ready for your adventure!</li>
                        <li>Contact us 24/7 for any changes</li>
                    </ul>
                    
                    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(0, 212, 255, 0.3);">
                        <p style="color: rgba(255, 255, 255, 0.7);">TravelGo © 2026 | Your Trusted Travel Companion</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=html_body
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_special_offer_email(user_email, user_name, offer_details):
    """Send special offer/deal email"""
    try:
        subject = f"🎁 Special Offer: {offer_details.get('title', 'Travel Deal')}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background: linear-gradient(135deg, #0a0e27 0%, #1a1f4b 50%, #0f0c29 100%); color: #fff; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 30px; backdrop-filter: blur(10px);">
                    <h1 style="color: #ff006e; text-align: center; margin-bottom: 20px;">🎁 Exclusive Offer for You!</h1>
                    <p style="text-align: center; font-size: 18px; font-weight: bold; color: #00d4ff;">
                        {offer_details.get('title', 'Special Deal')}
                    </p>
                    
                    <div style="background: linear-gradient(135deg, #ff006e, #ff6b6b); padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;">
                        <p style="font-size: 32px; font-weight: bold; margin: 0;">{offer_details.get('discount', '30%')} OFF</p>
                        <p style="margin: 10px 0 0 0;">Valid until {offer_details.get('expires', 'Dec 31')}</p>
                    </div>
                    
                    <p style="color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
                        {offer_details.get('description', 'Get amazing travel deals today!')}
                    </p>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="http://localhost:5000/offers" style="background: linear-gradient(135deg, #00d4ff, #7b2ff7); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: bold;">
                            View Offer
                        </a>
                    </div>
                </div>
            </body>
        </html>
        """
        
        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=html_body
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_welcome_email(user_email, user_name):
    """Send welcome email to new users"""
    try:
        subject = "Welcome to TravelGo - Your Travel Journey Begins! 🌍"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background: linear-gradient(135deg, #0a0e27 0%, #1a1f4b 50%, #0f0c29 100%); color: #fff; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 30px; backdrop-filter: blur(10px);">
                    <h1 style="color: #00d4ff; text-align: center;">Welcome to TravelGo, {user_name}! ✈️</h1>
                    
                    <p style="color: rgba(255, 255, 255, 0.9); font-size: 16px; line-height: 1.8;">
                        We're thrilled to have you on board! TravelGo is your personal travel companion, 
                        helping you discover, book, and experience amazing destinations around the world.
                    </p>
                    
                    <h2 style="color: #7b2ff7; margin-top: 30px;">Get Started With:</h2>
                    <ul style="color: rgba(255, 255, 255, 0.8); font-size: 16px; line-height: 1.8;">
                        <li>🏨 <strong>Book Hotels</strong> - Find accommodations at great prices</li>
                        <li>✈️ <strong>Search Flights</strong> - Compare and book flights</li>
                        <li>🚗 <strong>Rent Vehicles</strong> - Explore destinations with rental cars</li>
                        <li>⭐ <strong>Read Reviews</strong> - Get insights from travelers</li>
                        <li>❤️ <strong>Build Wishlist</strong> - Save your favorite trips</li>
                    </ul>
                    
                    <div style="border: 2px solid #00d4ff; border-radius: 10px; padding: 20px; margin: 30px 0; background: rgba(0, 212, 255, 0.1);">
                        <h3 style="color: #00d4ff; margin-top: 0;">🎉 Exclusive Welcome Bonus!</h3>
                        <p style="color: rgba(255, 255, 255, 0.9);">
                            Get <strong style="color: #00d4ff;">20% OFF</strong> on your first booking! 
                            Use code: <strong>WELCOME20</strong>
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="http://localhost:5000/dashboard" style="background: linear-gradient(135deg, #00d4ff, #7b2ff7); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: bold;">
                            Start Exploring
                        </a>
                    </div>
                </div>
            </body>
        </html>
        """
        
        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=html_body
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({"email": email})

        if user:
            return "User already exists"

        users.insert_one({
            "name": name,
            "email": email,
            "password": password,
            "created_at": datetime.now(),
            "rating": 0,
            "total_bookings": 0
        })
        
        # Send welcome email
        send_welcome_email(email, name)

        return redirect('/login')

    return render_template("register.html")


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        try:
            user = users.find_one({"email": email, "password": password})
        except Exception:
            return redirect('/error/database')

        if user:
            session['user'] = email
            session['user_name'] = user.get('name', 'User')
            return redirect('/dashboard')

        return redirect('/error/invalid-login')

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    return render_template("dashboard.html", last_location=session.get('last_location'))


@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    
    user = users.find_one({"email": session['user']})
    user_bookings = list(bookings.find({"user": session['user']}))
    
    return render_template("profile.html", user=user, total_bookings=len(user_bookings))


@app.route('/notifications')
def notifications():
    if 'user' not in session:
        return redirect('/login')
    
    notifications_list = [
        {"type": "booking", "message": "Your booking to Paris is confirmed!", "date": "2 hours ago"},
        {"type": "offer", "message": "Special offer: 30% off on European destinations", "date": "1 day ago"},
        {"type": "review", "message": "Rate your recent trip to Barcelona", "date": "3 days ago"}
    ]
    
    return render_template("notifications.html", notifications=notifications_list)


@app.route('/offers')
def offers():
    if 'user' not in session:
        return redirect('/login')
    
    offers_list = [
        {"destination": "Paris", "discount": "30%", "price": "₹70,550"},
        {"destination": "Tokyo", "discount": "25%", "price": "₹99,600"},
        {"destination": "dubai", "discount": "40%", "price": "₹53,950"},
        {"destination": "Barcelona", "discount": "20%", "price": "₹64,740"}
    ]
    
    return render_template("offers.html", offers=offers_list)


@app.route('/tips')
def tips():
    if 'user' not in session:
        return redirect('/login')
    
    tips_list = [
        {"title": "Pack Light", "description": "Bring only what you need to travel comfortably", "icon": "🎒"},
        {"title": "Travel Off-Season", "description": "Save money by traveling during low season", "icon": "💰"},
        {"title": "Learn Basic Phrases", "description": "Master essential phrases in local languages", "icon": "🗣️"},
        {"title": "Use Local Transport", "description": "Experience real culture using public transportation", "icon": "🚌"}
    ]
    
    return render_template("tips.html", tips=tips_list)


@app.route('/search', methods=['GET','POST'])
def search():

    if 'user' not in session:
        return redirect('/login')

    source_data = request.form if request.method == 'POST' else request.args

    destination = source_data.get('destination', '').strip()
    budget = source_data.get('budget', '')
    category = source_data.get('category', '')
    travelers = source_data.get('travelers', '1')

    # If no filters on GET, keep original landing behavior
    if request.method == 'GET' and not any([destination, budget, category]):
        return render_template("search.html", plans=None)

    # Build filter query for plans
    query = {}
    if destination:
        query['destination'] = {'$regex': destination, '$options': 'i'}
    if budget:
        query['budget'] = budget
    if category:
        query['category'] = category

    matching_plans = enrich_plan_images(list(plans.find(query)))

    return render_template("search.html", plans=matching_plans,
                           search_params=source_data, travelers=int(travelers))


@app.route('/plans')
def view_plans():
    if 'user' not in session:
        return redirect('/login')

    all_plans = enrich_plan_images(list(plans.find()))
    return render_template("search.html", plans=all_plans, show_all=True)


@app.route('/book-plan', methods=['POST'])
def book_plan():
    if 'user' not in session:
        return redirect('/login')

    plan_id = request.form.get('plan_id', '')
    travelers = request.form.get('travelers', '1')
    travel_date = request.form.get('travel_date', '')

    plan = plans.find_one({"plan_id": plan_id})
    if not plan:
        return redirect('/search')

    total_price = plan['price'] * int(travelers)

    booking_data = {
        "plan_id": plan_id,
        "plan_name": plan['name'],
        "destination": plan['destination'],
        "duration": plan['duration'],
        "price_per_person": str(plan['price']),
        "total_price": str(total_price),
        "travelers": travelers,
        "travel_date": travel_date,
    }
    amount = format_inr(total_price)
    session['pending_booking'] = booking_data
    session['pending_booking_type'] = 'plan'
    session['pending_amount'] = amount
    return redirect('/payment')


@app.route('/bookings')
def view_bookings():

    if 'user' not in session:
        return redirect('/login')

    user_bookings = list(bookings.find({"user": session['user']}))

    return render_template("bookings.html", bookings=user_bookings)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_name', None)
    return redirect('/')


@app.route('/api/booking-stats')
def booking_stats():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        user_bookings = list(bookings.find({"user": session['user']}))
        user = users.find_one({"email": session['user']})
    except Exception:
        return jsonify({
            "error": "Database connection error",
            "redirect": "/error/database"
        }), 500
    
    return jsonify({
        "total_bookings": len(user_bookings),
        "countries_visited": 12,
        "total_spent": 2450,
        "rating": user.get('rating', 0) if user else 0
    })


# HOTELS ROUTE
@app.route('/hotels', methods=['GET', 'POST'])
def hotels():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        destination = request.form.get('destination', '')
        check_in = request.form.get('check_in', '')
        check_out = request.form.get('check_out', '')
        price_range = request.form.get('price_range', 'moderate')
        
        # Sample hotels data
        hotels_list = [
            {
                "id": str(uuid.uuid4()),
                "name": "Luxury Palace Hotel",
                "destination": "Paris",
                "price": "₹20,750",
                "rating": "4.8",
                "image_url": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?auto=format&fit=crop&w=1200&q=80",
                "beds": "1 King Bed",
                "amenities": "WiFi, Pool, Spa, Restaurant"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Ocean View Resort",
                "destination": "Maldives",
                "price": "₹14,940",
                "rating": "4.9",
                "image_url": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?auto=format&fit=crop&w=1200&q=80",
                "beds": "1 Double Bed",
                "amenities": "Beach Access, Water Sports, WiFi"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Mountain Lodge",
                "destination": "Swiss Alps",
                "price": "₹12,450",
                "rating": "4.7",
                "image_url": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=1200&q=80",
                "beds": "2 Single Beds",
                "amenities": "Mountain View, Fireplace, Restaurant"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "City Center Inn",
                "destination": "Tokyo",
                "price": "₹9,960",
                "rating": "4.6",
                "image_url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=1200&q=80",
                "beds": "1 Twin Bed",
                "amenities": "WiFi, Restaurant, Business Center"
            }
        ]
        
        return render_template("hotels.html", hotels=hotels_list, search_params=request.form)
    
    return render_template("hotels.html", hotels=[])


# FLIGHTS ROUTE
@app.route('/flights', methods=['GET', 'POST'])
def flights():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        from_city = request.form.get('from_city', '')
        to_city = request.form.get('to_city', '')
        departure = request.form.get('departure', '')
        passengers = request.form.get('passengers', '1')
        
        # Sample flights data
        flights_list = [
            {
                "id": str(uuid.uuid4()),
                "airline": "Sky Airlines",
                "from": from_city or "New York",
                "to": to_city or "London",
                "departure": "10:30 AM",
                "arrival": "11:00 PM",
                "duration": "7h 30m",
                "price": "₹37,350",
                "seats": "145",
                "rating": "4.5",
                "stops": "Non-stop"
            },
            {
                "id": str(uuid.uuid4()),
                "airline": "Global Airways",
                "from": from_city or "New York",
                "to": to_city or "London",
                "departure": "2:15 PM",
                "arrival": "1:45 AM",
                "duration": "7h 30m",
                "price": "₹31,540",
                "seats": "89",
                "rating": "4.3",
                "stops": "Non-stop"
            },
            {
                "id": str(uuid.uuid4()),
                "airline": "Premium Air",
                "from": from_city or "New York",
                "to": to_city or "London",
                "departure": "6:00 PM",
                "arrival": "5:30 AM",
                "duration": "7h 30m",
                "price": "₹43,160",
                "seats": "220",
                "rating": "4.8",
                "stops": "Non-stop"
            }
        ]
        
        return render_template("flights.html", flights=flights_list, search_params=request.form)
    
    return render_template("flights.html", flights=[])


# BOOK FLIGHT - redirect to payment page
@app.route('/book-flight', methods=['POST'])
def book_flight():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    booking_data = {
        "airline": request.form.get('airline', ''),
        "from_city": request.form.get('from_city', ''),
        "to_city": request.form.get('to_city', ''),
        "departure": request.form.get('departure', ''),
        "arrival": request.form.get('arrival', ''),
        "duration": request.form.get('duration', ''),
        "price": request.form.get('price', ''),
        "passengers": request.form.get('passengers', '1'),
    }
    amount = request.form.get('price', '$0')
    session['pending_booking'] = booking_data
    session['pending_booking_type'] = 'flight'
    session['pending_amount'] = amount
    return redirect('/payment')


# REVIEWS ROUTE
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        destination = request.form.get('destination', '')
        rating = request.form.get('rating', '5')
        review_text = request.form.get('review', '')
        
        user = users.find_one({"email": session['user']})
        
        if reviews_collection:
            reviews_collection.insert_one({
                "user": session['user'],
                "user_name": session.get('user_name', 'Anonymous'),
                "destination": destination,
                "rating": int(rating),
                "text": review_text,
                "created_at": datetime.now()
            })
        
        return redirect('/reviews')
    
    # Get reviews
    reviews_list = []
    if reviews_collection:
        reviews_list = list(reviews_collection.find())
    
    # Sample reviews if collection is empty
    if not reviews_list:
        reviews_list = [
            {
                "user_name": "John Smith",
                "destination": "Paris",
                "rating": "5",
                "text": "Amazing experience! The Eiffel Tower is breathtaking. Highly recommend visiting in spring.",
                "created_at": "2 weeks ago"
            },
            {
                "user_name": "Sarah Johnson",
                "destination": "Tokyo",
                "rating": "4",
                "text": "Great city with amazing food and culture. A bit crowded in some areas but worth exploring.",
                "created_at": "1 month ago"
            }
        ]
    
    return render_template("reviews.html", reviews=reviews_list)


# WISHLIST ROUTE
@app.route('/wishlist')
def wishlist():
    if 'user' not in session:
        return redirect('/login')
    
    # Sample wishlist items
    wishlist_items = [
        {
            "id": str(uuid.uuid4()),
            "name": "Paris City Tour",
            "price": "₹70,550",
            "image": "🗼",
            "saved_date": "5 days ago"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Tokyo Tech Experience",
            "price": "₹99,600",
            "image": "🗾",
            "saved_date": "2 weeks ago"
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Dubai Luxury Package",
            "price": "₹1,24,500",
            "image": "🌆",
            "saved_date": "3 weeks ago"
        }
    ]
    
    return render_template("wishlist.html", wishlist=wishlist_items)


# ADD TO WISHLIST API
@app.route('/api/add-to-wishlist', methods=['POST'])
def add_to_wishlist():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    
    if wishlist_collection:
        wishlist_collection.insert_one({
            "user": session['user'],
            "item": data.get('item'),
            "price": data.get('price'),
            "created_at": datetime.now()
        })
    
    return jsonify({"success": True, "message": "Added to wishlist!"})


@app.route('/api/location', methods=['GET', 'POST'])
def api_location():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'GET':
        return jsonify({"success": True, "location": session.get('last_location')})

    data = request.get_json(silent=True) or {}

    try:
        latitude = float(data.get('latitude')) if data.get('latitude') is not None else None
        longitude = float(data.get('longitude')) if data.get('longitude') is not None else None
        accuracy = float(data.get('accuracy')) if data.get('accuracy') is not None else None
    except (TypeError, ValueError):
        return jsonify({"success": False, "message": "Invalid location payload"}), 400

    if latitude is None or longitude is None:
        return jsonify({"success": False, "message": "Latitude and longitude are required"}), 400

    location_doc = {
        "latitude": round(latitude, 6),
        "longitude": round(longitude, 6),
        "accuracy": round(accuracy, 2) if accuracy is not None else None,
        "label": data.get('label', ''),
        "updated_at": datetime.now().isoformat()
    }

    session['last_location'] = location_doc
    return jsonify({"success": True, "location": location_doc})


# BOOK HOTEL - redirect to payment page
@app.route('/book-hotel', methods=['POST'])
def book_hotel():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    booking_data = {
        "hotel_name": request.form.get('hotel_name', ''),
        "check_in": request.form.get('check_in', ''),
        "check_out": request.form.get('check_out', ''),
        "rooms": request.form.get('rooms', '1'),
        "price": request.form.get('price', '$0'),
    }
    amount = request.form.get('price', '$0')
    session['pending_booking'] = booking_data
    session['pending_booking_type'] = 'hotel'
    session['pending_amount'] = amount
    return redirect('/payment')


# BOOKING CONFIRMATION
@app.route('/booking-confirmation/<booking_id>')
def booking_confirmation(booking_id):
    if 'user' not in session:
        return redirect('/login')
    
    booking = bookings.find_one({"booking_id": booking_id, "user": session['user']})
    
    if not booking:
        return redirect('/bookings')
    
    return render_template("booking_confirmation.html", booking=booking)


# VEHICLE RENTAL ROUTES
def get_vehicle_catalog():
    return [
        {
            "id": "toyota-corolla",
            "name": "Toyota Corolla",
            "type": "Economy",
            "price": "₹2,905",
            "price_per_day": "₹2,905",
            "image_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1200&q=80",
            "transmission": "Automatic",
            "passengers": "5",
            "luggage": "2 bags",
            "fuel": "Petrol",
            "rating": "4.7",
            "mileage": "Unlimited",
            "description": "A practical city sedan with excellent fuel efficiency, smooth handling, and enough comfort for daily commuting or weekend getaways.",
            "features": [
                "Air Conditioning",
                "Power Steering",
                "ABS Brakes",
                "Bluetooth Audio",
                "USB Charging",
                "Rear Parking Camera"
            ],
            "insurance": "Full coverage",
            "cancellation": "Free cancellation up to 24 hours",
            "pickup_locations": ["Airport", "City Center", "Railway Station"],
            "reviews": [
                {"user": "John D.", "rating": "5", "text": "Very clean and easy to drive in city traffic."},
                {"user": "Sarah M.", "rating": "4", "text": "Great value and smooth pickup process."}
            ]
        },
        {
            "id": "bmw-3-series",
            "name": "BMW 3 Series",
            "type": "Luxury",
            "price": "₹7,055",
            "price_per_day": "₹7,055",
            "image_url": "https://images.unsplash.com/photo-1616455579100-2ceaa4eb2d37?auto=format&fit=crop&w=1200&q=80",
            "transmission": "Automatic",
            "passengers": "5",
            "luggage": "3 bags",
            "fuel": "Petrol",
            "rating": "4.9",
            "mileage": "Unlimited",
            "description": "A sporty luxury sedan offering premium interiors, strong performance, and refined ride quality for executive travel.",
            "features": [
                "Leather Seats",
                "Dual-Zone Climate",
                "Sunroof",
                "Premium Sound",
                "Cruise Control",
                "Lane Assist"
            ],
            "insurance": "Premium coverage",
            "cancellation": "Free cancellation up to 48 hours",
            "pickup_locations": ["Airport", "Downtown", "Business District"],
            "reviews": [
                {"user": "Alex T.", "rating": "5", "text": "Excellent condition and fantastic drive quality."},
                {"user": "Priya K.", "rating": "5", "text": "Perfect for a premium city and highway trip."}
            ]
        },
        {
            "id": "volkswagen-passat",
            "name": "Volkswagen Passat",
            "type": "Premium",
            "price": "₹5,395",
            "price_per_day": "₹5,395",
            "image_url": "https://images.unsplash.com/photo-1542282088-fe8426682b8f?auto=format&fit=crop&w=1200&q=80",
            "transmission": "Automatic",
            "passengers": "5",
            "luggage": "2 bags",
            "fuel": "Diesel",
            "rating": "4.8",
            "mileage": "Unlimited",
            "description": "A balanced premium sedan with spacious cabin comfort, efficient touring capability, and dependable road performance.",
            "features": [
                "Auto Climate Control",
                "Touchscreen Infotainment",
                "Cruise Control",
                "Parking Sensors",
                "Push Start",
                "Rear AC Vents"
            ],
            "insurance": "Comprehensive coverage",
            "cancellation": "Free cancellation up to 24 hours",
            "pickup_locations": ["Airport", "City Center", "Hotel Delivery"],
            "reviews": [
                {"user": "Ritika S.", "rating": "5", "text": "Comfortable ride for long routes."},
                {"user": "Daniel P.", "rating": "4", "text": "Good premium option at a fair daily price."}
            ]
        },
        {
            "id": "chevrolet-spark",
            "name": "Chevrolet Spark",
            "type": "Economy",
            "price": "₹2,490",
            "price_per_day": "₹2,490",
            "image_url": "https://images.unsplash.com/photo-1549924231-f129b911e442?auto=format&fit=crop&w=1200&q=80",
            "transmission": "Manual",
            "passengers": "4",
            "luggage": "1 bag",
            "fuel": "Petrol",
            "rating": "4.5",
            "mileage": "Unlimited",
            "description": "A compact and budget-friendly hatchback, ideal for short city rides, easy parking, and low fuel cost travel.",
            "features": [
                "Compact Design",
                "Power Windows",
                "Bluetooth",
                "ABS Brakes",
                "Foldable Rear Seats",
                "Child Lock"
            ],
            "insurance": "Standard coverage",
            "cancellation": "Free cancellation up to 24 hours",
            "pickup_locations": ["City Center", "Metro Hub", "Railway Station"],
            "reviews": [
                {"user": "Nikhil A.", "rating": "4", "text": "Great for city use and tight streets."},
                {"user": "Emma R.", "rating": "5", "text": "Affordable and surprisingly comfortable."}
            ]
        },
        {
            "id": "honda-crv",
            "name": "Honda CR-V",
            "type": "SUV",
            "price": "₹5,810",
            "price_per_day": "₹5,810",
            "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1200&q=80",
            "transmission": "Automatic",
            "passengers": "7",
            "luggage": "4 bags",
            "fuel": "Petrol",
            "rating": "4.8",
            "mileage": "Unlimited",
            "description": "A family-friendly SUV with roomy seating, stable highway handling, and strong comfort for group or mountain travel.",
            "features": [
                "7-Seater Comfort",
                "Rear AC",
                "Large Cargo Space",
                "All-Terrain Modes",
                "Cruise Control",
                "Reverse Camera"
            ],
            "insurance": "Comprehensive SUV coverage",
            "cancellation": "Free cancellation up to 24 hours",
            "pickup_locations": ["Airport", "City Center", "Resort Pickup"],
            "reviews": [
                {"user": "Kabir V.", "rating": "5", "text": "Perfect SUV for a family road trip."},
                {"user": "Maya L.", "rating": "4", "text": "Spacious and easy to handle despite size."}
            ]
        },
        {
            "id": "mercedes-c-class",
            "name": "Mercedes-Benz C-Class",
            "type": "Luxury",
            "price": "₹7,885",
            "price_per_day": "₹7,885",
            "image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=1200&q=80",
            "transmission": "Automatic",
            "passengers": "5",
            "luggage": "3 bags",
            "fuel": "Petrol",
            "rating": "4.9",
            "mileage": "Unlimited",
            "description": "A premium executive sedan delivering high-end comfort, smooth performance, and a luxury in-cabin experience.",
            "features": [
                "Leather Interior",
                "Ambient Lighting",
                "Panoramic Sunroof",
                "Premium Navigation",
                "Wireless Charging",
                "Advanced Driver Assist"
            ],
            "insurance": "Premium executive coverage",
            "cancellation": "Free cancellation up to 48 hours",
            "pickup_locations": ["Airport", "Business District", "Hotel Delivery"],
            "reviews": [
                {"user": "Arjun N.", "rating": "5", "text": "Luxury at its best. Extremely smooth drive."},
                {"user": "Sophie G.", "rating": "5", "text": "Immaculate car and very professional service."}
            ]
        },
        {
            "id": "volvo-9400-bus",
            "name": "Volvo 9400 Intercity",
            "type": "Bus",
            "price": "₹1,245",
            "price_per_day": "₹1,245",
            "pricing_unit": "/seat",
            "image_url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1200&q=80",
            "transmission": "Automatic",
            "passengers": "40",
            "luggage": "15 kg per seat",
            "fuel": "Diesel",
            "rating": "4.6",
            "mileage": "Point-to-point route",
            "description": "Comfortable long-distance AC coach with reclining seats, charging ports, and onboard Wi-Fi for intercity travel.",
            "features": [
                "Recliner Seats",
                "Air Suspension",
                "Onboard Wi-Fi",
                "Mobile Charging",
                "CCTV Safety",
                "Live GPS Tracking"
            ],
            "insurance": "Passenger travel coverage",
            "cancellation": "Free cancellation up to 12 hours",
            "pickup_locations": ["Main Bus Terminal", "Airport Bus Bay", "City Pickup Point"],
            "reviews": [
                {"user": "Rahul S.", "rating": "5", "text": "Clean bus, punctual departure, and very comfortable seats."},
                {"user": "Neha P.", "rating": "4", "text": "Good journey and smooth booking experience."}
            ]
        },
        {
            "id": "vistadome-express-train",
            "name": "Vistadome Express",
            "type": "Train",
            "price": "₹1,780",
            "price_per_day": "₹1,780",
            "pricing_unit": "/seat",
            "image_url": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=1200&q=80",
            "transmission": "Electric",
            "passengers": "72",
            "luggage": "20 kg per seat",
            "fuel": "Electric",
            "rating": "4.8",
            "mileage": "Intercity express route",
            "description": "Premium scenic train experience with panoramic windows, wider seats, and reliable high-speed connectivity between major cities.",
            "features": [
                "Panoramic Windows",
                "Wide Recliner Seats",
                "Onboard Pantry",
                "Charging Ports",
                "Clean Washrooms",
                "Real-Time Route Updates"
            ],
            "insurance": "Rail passenger coverage",
            "cancellation": "Free cancellation up to 24 hours",
            "pickup_locations": ["Central Station", "North Junction", "Airport Rail Link"],
            "reviews": [
                {"user": "Karan B.", "rating": "5", "text": "Scenic and comfortable train journey, worth it."},
                {"user": "Aditi M.", "rating": "4", "text": "Excellent service and on-time arrival."}
            ]
        }
    ]


def get_transport_seat_plan(vehicle):
    transport_type = vehicle.get('type', '').lower()

    if transport_type == 'bus':
        occupied = {'A2', 'D3', 'B5', 'C7', 'A9'}
        seat_rows = []
        for row in range(1, 11):
            seats = []
            for seat_code in ['A', 'B', 'C', 'D']:
                seat_id = f"{seat_code}{row}"
                seats.append({
                    "id": seat_id,
                    "label": seat_id,
                    "available": seat_id not in occupied
                })
            seat_rows.append({"row": row, "seats": seats})

        return {
            "mode": "bus",
            "title": "Bus Seat Selection",
            "description": "Choose your preferred seats like a theatre layout.",
            "seat_rows": seat_rows,
            "max_select": 5
        }

    if transport_type == 'train':
        occupied = {'A1', 'C2', 'F3', 'D4', 'B6', 'E8'}
        seat_rows = []
        for row in range(1, 9):
            seats = []
            for seat_code in ['A', 'B', 'C', 'D', 'E', 'F']:
                seat_id = f"{seat_code}{row}"
                seats.append({
                    "id": seat_id,
                    "label": seat_id,
                    "available": seat_id not in occupied
                })
            seat_rows.append({"row": row, "seats": seats})

        return {
            "mode": "train",
            "title": "Train Berth/Seat Selection",
            "description": "Pick available train seats before continuing to payment.",
            "seat_rows": seat_rows,
            "max_select": 6
        }

    passenger_capacity = ''.join(ch for ch in vehicle.get('passengers', '5') if ch.isdigit())
    passenger_capacity = int(passenger_capacity) if passenger_capacity else 5
    max_select = max(1, min(6, passenger_capacity - 1))

    car_seats = [
        {"id": "DR", "label": "Driver", "available": False},
        {"id": "F1", "label": "Front", "available": True},
        {"id": "R1", "label": "Rear Left", "available": True},
        {"id": "R2", "label": "Rear Middle", "available": True},
        {"id": "R3", "label": "Rear Right", "available": True}
    ]

    if passenger_capacity >= 7:
        car_seats.extend([
            {"id": "T1", "label": "Third Left", "available": True},
            {"id": "T2", "label": "Third Right", "available": True}
        ])

    return {
        "mode": "car",
        "title": "Passenger Seat Selection",
        "description": "Choose passenger seats for this transport plan.",
        "car_seats": car_seats,
        "max_select": max_select
    }


@app.route('/vehicles', methods=['GET', 'POST'])
def vehicles():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        location = request.form.get('location', '')
        destination = request.form.get('destination', '')
        pickup_date = request.form.get('pickup_date', '')
        return_date = request.form.get('return_date', '')
        vehicle_type = request.form.get('vehicle_type', 'all').strip().lower()
        
        vehicles_list = get_vehicle_catalog()
        if vehicle_type and vehicle_type != 'all':
            vehicles_list = [
                vehicle for vehicle in vehicles_list
                if vehicle.get('type', '').lower() == vehicle_type.lower()
            ]
        
        return render_template("vehicles.html", vehicles=vehicles_list, search_params=request.form)
    
    return render_template("vehicles.html", vehicles=[])


@app.route('/book-vehicle', methods=['POST'])
def book_vehicle():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    booking_data = {
        "vehicle_name": request.form.get('vehicle_name', ''),
        "pickup_date": request.form.get('pickup_date', ''),
        "return_date": request.form.get('return_date', ''),
        "location": request.form.get('location', ''),
        "destination": request.form.get('destination', ''),
        "price": request.form.get('price', '$0'),
        "seat_selection": request.form.get('seat_selection', ''),
        "transport_type": request.form.get('transport_type', ''),
    }
    amount = request.form.get('price', '$0')
    session['pending_booking'] = booking_data
    session['pending_booking_type'] = 'vehicle'
    session['pending_amount'] = amount
    return redirect('/payment')


@app.route('/vehicle-details/<vehicle_id>')
def vehicle_details(vehicle_id):
    if 'user' not in session:
        return redirect('/login')
    
    vehicle = next(
        (item for item in get_vehicle_catalog() if item['id'] == vehicle_id),
        None
    )
    if not vehicle:
        return redirect('/vehicles')
    
    return render_template("vehicle_details.html", vehicle=vehicle)


@app.route('/transport-seats/<vehicle_id>')
def transport_seats(vehicle_id):
    if 'user' not in session:
        return redirect('/login')

    vehicle = next(
        (item for item in get_vehicle_catalog() if item['id'] == vehicle_id),
        None
    )
    if not vehicle:
        return redirect('/vehicles')

    seat_plan = get_transport_seat_plan(vehicle)

    return render_template(
        "transport_seats.html",
        vehicle=vehicle,
        seat_plan=seat_plan,
        search_params=request.args
    )


# PAYMENT PAGE
@app.route('/payment')
def payment():
    if 'user' not in session:
        return redirect('/login')

    booking_data = session.get('pending_booking', {})
    booking_type = session.get('pending_booking_type', '')
    amount = session.get('pending_amount', '$0')

    if not booking_data or not booking_type:
        return redirect('/dashboard')

    return render_template("payment.html",
                           booking_data=booking_data,
                           booking_type=booking_type,
                           amount=amount)


# PROCESS PAYMENT - actually creates the booking
@app.route('/process-payment', methods=['POST'])
def process_payment():
    if 'user' not in session:
        return redirect('/login')

    booking_data = session.get('pending_booking', {})
    booking_type = session.get('pending_booking_type', '')
    payment_method = request.form.get('payment_method', 'upi')

    if not booking_data or not booking_type:
        return redirect('/dashboard')

    booking_id = str(uuid.uuid4())
    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    payment_details = {
        "amount": session.get('pending_amount', '$0'),
        "status": "paid",
        "transaction_id": transaction_id,
        "paid_at": datetime.now()
    }

    if payment_method == 'upi':
        payment_details["upi_id"] = request.form.get('upi_id', '')
    elif payment_method == 'net_banking':
        payment_details["bank"] = request.form.get('bank') or request.form.get('other_bank', '')
    elif payment_method == 'wallet':
        payment_details["wallet"] = request.form.get('wallet', '')
        payment_details["wallet_phone"] = request.form.get('wallet_phone', '')

    if booking_type == 'hotel':
        booking_doc = {
            "booking_id": booking_id,
            "user": session['user'],
            "type": "hotel",
            "name": booking_data.get('hotel_name', ''),
            "check_in": booking_data.get('check_in', ''),
            "check_out": booking_data.get('check_out', ''),
            "rooms": int(booking_data.get('rooms', 1)),
            "payment_method": payment_method,
            "payment_details": payment_details,
            "transaction_id": transaction_id,
            "status": "confirmed",
            "created_at": datetime.now()
        }
    elif booking_type == 'flight':
        booking_doc = {
            "booking_id": booking_id,
            "user": session['user'],
            "type": "flight",
            "airline": booking_data.get('airline', ''),
            "from_city": booking_data.get('from_city', ''),
            "to_city": booking_data.get('to_city', ''),
            "departure": booking_data.get('departure', ''),
            "arrival": booking_data.get('arrival', ''),
            "duration": booking_data.get('duration', ''),
            "price": booking_data.get('price', ''),
            "passengers": int(booking_data.get('passengers', 1)),
            "payment_method": payment_method,
            "payment_details": payment_details,
            "transaction_id": transaction_id,
            "status": "confirmed",
            "created_at": datetime.now()
        }
    elif booking_type == 'vehicle':
        booking_doc = {
            "booking_id": booking_id,
            "user": session['user'],
            "type": "vehicle",
            "vehicle_name": booking_data.get('vehicle_name', ''),
            "pickup_date": booking_data.get('pickup_date', ''),
            "return_date": booking_data.get('return_date', ''),
            "location": booking_data.get('location', ''),
            "destination": booking_data.get('destination', ''),
            "payment_method": payment_method,
            "payment_details": payment_details,
            "transaction_id": transaction_id,
            "status": "confirmed",
            "created_at": datetime.now()
        }
    elif booking_type == 'plan':
        plan = plans.find_one({"plan_id": booking_data.get('plan_id', '')})
        booking_doc = {
            "booking_id": booking_id,
            "user": session['user'],
            "type": "plan",
            "plan_name": booking_data.get('plan_name', ''),
            "destination": booking_data.get('destination', ''),
            "duration": booking_data.get('duration', ''),
            "price_per_person": int(booking_data.get('price_per_person', 0)),
            "total_price": int(booking_data.get('total_price', 0)),
            "travelers": int(booking_data.get('travelers', 1)),
            "travel_date": booking_data.get('travel_date', ''),
            "includes": plan.get('includes', []) if plan else [],
            "payment_method": payment_method,
            "payment_details": payment_details,
            "transaction_id": transaction_id,
            "status": "confirmed",
            "created_at": datetime.now()
        }
    else:
        return redirect('/dashboard')

    bookings.insert_one(booking_doc)

    # Send confirmation email
    user = users.find_one({"email": session['user']})
    if user:
        send_booking_confirmation_email(
            session['user'],
            user.get('name', 'Traveler'),
            booking_doc
        )

    # Clear pending booking from session
    session.pop('pending_booking', None)
    session.pop('pending_booking_type', None)
    session.pop('pending_amount', None)

    return redirect(f'/booking-confirmation/{booking_id}')


@app.errorhandler(400)
def bad_request(error):
    return render_error_page(
        400,
        "Invalid Request",
        "The request could not be processed. Please verify your input and try again.",
        400,
    )


@app.errorhandler(404)
def not_found(error):
    return render_error_page(
        404,
        "Page Not Found",
        "The page you are looking for does not exist or has been moved.",
        404,
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return render_error_page(
        405,
        "Invalid Request Method",
        "This action is not allowed for the requested page.",
        405,
    )


@app.errorhandler(500)
def internal_server_error(error):
    message = "An unexpected server error occurred. Please try again."
    if "credential" in str(error).lower() or "database" in str(error).lower():
        message = "TravelGo could not connect to the database. Please verify database settings and try again."

    return render_error_page(
        500,
        "Server Error",
        message,
        500,
    )


if __name__ == '__main__':
    app.run(debug=True)