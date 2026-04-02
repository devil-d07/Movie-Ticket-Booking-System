# 🎬 Movie Ticket Booking System

A fully functional desktop application for booking movie tickets with a modern UI built using Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-Built--in-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 1. **User Authentication System** 👤
- User registration with validation
- Secure login system
- Password hashing using SHA-256
- Email and phone validation
- User profile management

### 2. **Movie Listing & Discovery** 🎥
- Browse available movies with detailed information
- Movie posters and genre information
- Duration, rating, and description display
- Responsive scrollable interface
- **Search functionality** - Find movies by title
- **Genre filtering** - Filter movies by genre
- Real-time search results

### 3. **Seat Selection System** 🪑
- Visual seat grid layout (10 rows × 15 columns)
- **Color-coded seats:**
  - 🟢 Green: Available seats
  - 🔴 Red: Booked seats
  - 🟡 Yellow: Selected seats
- Multiple showtime selection (4 showtimes per movie)
- Real-time seat availability updates
- Maximum 10 seats per booking
- Easy seat selection/deselection

### 4. **Booking & Payment** 💳
- Display complete booking summary
- Dynamic price calculation based on showtime
- Peak hour pricing (evening shows 7 PM - 10 PM)
- Booking confirmation with details
- Unique booking ID generation
- Transaction summary display

### 5. **Booking History** 🧾
- View all past bookings
- Complete booking details including:
  - Booking ID
  - Movie name
  - Showtime
  - Seat numbers
  - Amount paid
- Easy booking reference

### 6. **Database Management** 💾
- JSON-based data persistence
- Structured data for:
  - Movies (`data/movies.json`)
  - Users (`data/users.json`)
  - Bookings (`data/bookings.json`)
- No external database required
- Easy data backup and transfer

## 📁 Project Structure

```
movie_booking_app/
│
├── main.py                          # Application entry point
│
├── app/
│   ├── __init__.py                 # Package initialization
│   ├── gui.py                      # UI screens and layouts (Tkinter)
│   ├── booking.py                  # Booking logic and management
│   ├── database.py                 # JSON database operations
│   └── utils.py                    # Utility functions & validators
│
├── assets/
│   ├── images/
│   │   ├── movies/                 # Movie posters directory
│   │   ├── icons/                  # Icon images directory
│   │   └── seats/                  # Seat imagery directory
│
├── data/
│   ├── movies.json                 # Movie database
│   ├── users.json                  # User accounts database
│   └── bookings.json               # Booking records database
│
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd movie_booking_app

# Or download and extract the zip file
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python main.py
```

The application will launch in a new window.

## 📖 How to Use

### 1. **First Time Users**
- Click on **"Register"** button
- Fill in the registration form:
  - Username (3-20 alphanumeric characters)
  - Password (minimum 6 characters)
  - Email (valid email format)
  - Phone (10 digits)
- Click **"Register"** to create account

### 2. **Existing Users**
- Enter your username and password
- Click **"Login"** button

### 3. **Browse Movies**
- View all available movies
- **Search:** Use the search box to find movies by name
- **Filter:** Select a genre from the dropdown
- Click **"Book Tickets →"** on your desired movie

### 4. **Select Seats**
- Choose a **showtime** (4 options available)
- Click on **green seats** to select them
- Selected seats turn **yellow**
- Maximum 10 seats per booking
- View the selection summary below
- Click **"Proceed to Booking"** to continue

### 5. **Confirm Booking**
- Review booking details:
  - Movie name
  - Selected seats
  - Showtime
  - Passenger information
  - Total amount
- Click **"Confirm Booking"** to finalize
- View your booking confirmation with ID

### 6. **View Booking History**
- Click **"My Bookings"** from any screen where available
- See all your past bookings
- Booking IDs, seats, and amounts paid

## 💰 Pricing

- **Standard Rate:** ₹250 per seat
- **Peak Hours (7 PM - 10 PM):** ₹325 per seat (30% surcharge)

## 🎨 UI/UX Features

- **Modern Design:** Clean, professional interface
- **Color Scheme:** Red accent color (#e50914) matching movie theme
- **Responsive Layout:** Adapts to different window sizes
- **Intuitive Navigation:** Easy back buttons and clear workflows
- **Form Validation:** Real-time input validation with helpful messages
- **Visual Feedback:** Color-coded elements for clarity
- **Scrollable Content:** Support for large lists of movies/bookings

## 🔧 Technical Details

### Technologies Used
- **GUI Framework:** Tkinter (built-in with Python)
- **Image Processing:** Pillow (PIL)
- **Data Storage:** JSON files
- **Security:** SHA-256 password hashing
- **Architecture:** Object-Oriented Programming (OOP)

### Key Classes
- **`MovieBookingApp`** - Main application controller
- **`LoginRegisterScreen`** - Authentication UI
- **`MovieListingScreen`** - Browse and search movies
- **`SeatSelectionScreen`** - Select seats and showtimes
- **`BookingConfirmationScreen`** - Review and confirm bookings
- **`BookingHistoryScreen`** - View past bookings
- **`Database`** - JSON data persistence
- **`BookingManager`** - Booking logic and operations
- **`Validator`** - Input validation utilities
- **`PasswordManager`** - Password hashing
- **`PriceCalculator`** - Dynamic pricing logic

### Validation Rules
- **Username:** 3-20 characters, alphanumeric + underscore
- **Password:** Minimum 6 characters
- **Email:** Standard email format validation
- **Phone:** Exactly 10 digits
- **Seats:** A-J rows, columns 1-15

## 📊 Sample Data

The application comes with pre-loaded sample data:

### Movies Included:
1. **The Matrix Reloaded** (Sci-Fi)
2. **Inception** (Thriller)
3. **Interstellar** (Sci-Fi)
4. **The Dark Knight** (Action)
5. **Pulp Fiction** (Crime)

Each movie has:
- 4 showtimes daily
- Genre information
- Duration and rating
- Description

## 🔐 Security Features

- ✅ Password hashing (SHA-256)
- ✅ Input validation for all forms
- ✅ Prevention of double bookings
- ✅ Seat availability checking
- ✅ Unique booking IDs
- ✅ User-specific data isolation

## 📝 Sample Usage

```python
# Starting the application
python main.py

# User registration automatically creates:
# - User account in data/users.json
# - Entry in bookings.json with first booking

# Booking creates:
# - Unique booking ID: BK20260402143022
# - Timestamp of booking
# - Complete seat and movie information
```

## 🔄 Data Management

All data is stored in JSON format for easy access and modification:

```json
// Example booking record in bookings.json
{
  "booking_id": "BK20260402143022",
  "username": "john_doe",
  "movie_id": 2,
  "movie_title": "Inception",
  "show_time": "8:30 PM",
  "seats": ["A5", "A6", "B5"],
  "num_seats": 3,
  "total_cost": 975,
  "email": "john@example.com",
  "phone": "9876543210",
  "booking_date": "2026-04-02",
  "booking_time": "2026-04-02 14:30:22",
  "status": "confirmed"
}
```

## 🎯 Future Improvements

- [ ] Online payment integration (Razorpay, Stripe)
- [ ] Email ticket delivery
- [ ] SMS notifications
- [ ] Admin panel for movie management
- [ ] Movie ratings and reviews
- [ ] Promotional codes/discounts
- [ ] Seat diagram visualization with images
- [ ] Multiple languages support
- [ ] Dark/Light theme switching
- [ ] Booking cancellation functionality
- [ ] Database migration to SQL (SQLite, PostgreSQL)
- [ ] Backend API (Flask/Django)
- [ ] Mobile app version

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed
- Check if Pillow is installed: `pip install pillow`
- Verify file structure matches project layout

### Missing modules error
- Run: `pip install -r requirements.txt`
- Check `data/` folder exists with JSON files

### Seats showing as red when empty
- Refresh by selecting a different showtime and back
- Check `data/bookings.json` for conflicting entries

### Can't book seats
- Ensure you've selected a showtime first
- Check if too many seats are selected (max 10)
- Verify seats aren't already booked

## 📧 Contact & Support

For issues, improvements, or feature requests:
1. Check existing issues
2. Create a detailed bug report with screenshots
3. Include Python version and error messages

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with Tkinter - Python's standard GUI library
- Inspired by real-world movie ticket booking systems
- Made for educational and demonstration purposes

---

**Happy Booking! 🎬🎉**

Made with ❤️ for Python enthusiasts