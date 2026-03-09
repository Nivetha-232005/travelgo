# TravelGo - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Ensure MongoDB is Running
```bash
# On Windows
mongod

# On macOS (if installed via Homebrew)
brew services start mongodb-community

# On Linux
sudo systemctl start mongod
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Open in Browser
Visit: **http://localhost:5000**

---

## 📋 Checklist

- [x] Modern UI with gradient theme
- [x] Hotel booking system
- [x] Flight search
- [x] Reviews & ratings
- [x] Wishlist management
- [x] Enhanced dashboard
- [x] User authentication
- [x] Booking confirmation
- [x] Professional footers
- [x] Mobile responsive

---

## 🎯 Default Login Credentials

For testing purposes, register a new account or use sample data.

---

## ⚠️ Important Notes

1. **MongoDB Connection**: Ensure MongoDB is running on `localhost:27017`
2. **Secret Key**: Change `app.secret_key` in production
3. **Debug Mode**: Currently set to `True` - change to `False` in production
4. **Static Files**: CSS and JS are served from `/static` directory

---

## 🔧 Troubleshooting

### MongoDB Connection Error
```
Error: [Errno 111] Connection refused
Solution: Start MongoDB service (mongod)
```

### Port Already in Use
```
Error: Address already in use
Solution: Change port in app.py:
app.run(debug=True, port=5001)
```

### CSS Not Loading
```
Solution: Clear browser cache (Ctrl+Shift+Del)
Restart Flask server
```

---

## 📱 Mobile Responsiveness

All pages are fully responsive:
- Large screens (desktop/laptop)
- Medium screens (tablets)
- Small screens (mobile phones)

---

## 🎨 Customization

### Change Primary Color
Edit `style.css`:
```css
--primary-color: #00d4ff;  /* Change to your color */
```

### Change Company Name
Update in `app.py`:
```python
app.config['BRAND_NAME'] = 'Your Brand'
```

---

## 🌐 Features by Page

| Page | Features |
|------|----------|
| Index | Landing, Features, Stats, CTA |
| Dashboard | Analytics, Quick Links, Recommendations |
| Search | Advanced Filters, Results |
| Hotels | Search, Browse, Book, Wishlist |
| Flights | Compare, Filter, Book |
| Reviews | Write, Read, Rate |
| Wishlist | Save, Browse, Manage |
| Profile | Edit, Statistics |
| Offers | Browse, Filter, Purchase |
| Tips | Learn, Share, Articles |
| Notifications | Manage, Preferences |
| Bookings | View, Track, Manage |

---

## 💾 Database Collections

All collections are automatically created in MongoDB:

```
Database: travelgo
├── users
├── bookings
├── hotels
├── flights
├── reviews
└── wishlist
```

---

## 🔐 Security Tips

1. Use strong SECRET_KEY in production
2. Enable HTTPS in production
3. Validate all user inputs
4. Use environment variables for sensitive data
5. Implement rate limiting
6. Add CSRF protection

---

## 📧 Support & Feedback

- Documentation: See README.md
- Issues: Contact support team
- Features: Submit enhancement requests

---

## ✨ Enjoy TravelGo!

Start exploring the world with our beautiful travel platform. Happy travels! 🌍✈️
