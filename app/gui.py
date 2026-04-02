"""
GUI module for the movie booking application.
Implements the user interface with multiple screens using Tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from typing import Optional, List
from app.database import Database
from app.booking import BookingManager
from app.utils import Validator, PasswordManager, SeatHelper, PriceCalculator, DateTimeHelper


class MovieBookingApp:
    """Main application controller for the movie booking system."""

    def __init__(self, root: tk.Tk):
        """
        Initialize the main application.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # Initialize database and booking manager
        self.db = Database("data")
        self.booking_manager = BookingManager(self.db)
        self.current_user = None

        # Configure styles
        self._configure_styles()

        # Create frames
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Show login screen
        self.show_login_screen()

    def _configure_styles(self):
        """Configure Tkinter styles and colors."""
        self.colors = {
            "bg_dark": "#1a1a1a",
            "bg_light": "#f5f5f5",
            "accent": "#e50914",
            "accent_light": "#ff6b6b",
            "text_dark": "#333333",
            "text_light": "#ffffff",
            "success": "#28a745",
            "warning": "#ffc107",
            "danger": "#dc3545"
        }

    def clear_screen(self):
        """Clear the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Display the login/register screen."""
        self.clear_screen()
        LoginRegisterScreen(self.main_frame, self)

    def show_movie_listing(self):
        """Display the movie listing screen."""
        self.clear_screen()
        MovieListingScreen(self.main_frame, self)

    def show_seat_selection(self, movie_id: int):
        """Display the seat selection screen."""
        self.clear_screen()
        SeatSelectionScreen(self.main_frame, self, movie_id)

    def show_booking_confirmation(self, movie_id: int, seats: List[str], show_time: str):
        """Display the booking confirmation screen."""
        self.clear_screen()
        BookingConfirmationScreen(self.main_frame, self, movie_id, seats, show_time)

    def show_booking_history(self):
        """Display the user's booking history."""
        self.clear_screen()
        BookingHistoryScreen(self.main_frame, self)

    def logout(self):
        """Logout the current user."""
        self.current_user = None
        self.show_login_screen()


class LoginRegisterScreen:
    """Login and registration screen."""

    def __init__(self, parent: tk.Frame, app: MovieBookingApp):
        """
        Initialize login/register screen.

        Args:
            parent: Parent frame
            app: Main application instance
        """
        self.parent = parent
        self.app = app
        self.is_register = False

        # Main container
        self.container = tk.Frame(parent, bg=self.app.colors["bg_light"])
        self.container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(self.container, bg=self.app.colors["accent"], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_label = tk.Label(
            header,
            text="🎬 Movie Ticket Booking System",
            font=("Arial", 24, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"]
        )
        header_label.pack(pady=20)

        # Center frame for form
        center_frame = tk.Frame(self.container, bg=self.app.colors["bg_light"])
        center_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Form frame
        form_frame = tk.Frame(center_frame, bg=self.app.colors["text_light"], relief=tk.RAISED, bd=2)
        form_frame.pack(expand=False, fill=tk.BOTH, padx=20, pady=20, anchor=tk.CENTER, side=tk.TOP)

        # Title
        self.title_label = tk.Label(
            form_frame,
            text="Login",
            font=("Arial", 20, "bold"),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["text_dark"]
        )
        self.title_label.pack(pady=20)

        # Username
        tk.Label(form_frame, text="Username:", bg=self.app.colors["text_light"]).pack(anchor=tk.W, padx=30, pady=(10, 0))
        self.username_entry = tk.Entry(form_frame, font=("Arial", 11), width=35)
        self.username_entry.pack(padx=30, pady=(0, 15))

        # Password
        tk.Label(form_frame, text="Password:", bg=self.app.colors["text_light"]).pack(anchor=tk.W, padx=30, pady=(10, 0))
        self.password_entry = tk.Entry(form_frame, font=("Arial", 11), width=35, show="*")
        self.password_entry.pack(padx=30, pady=(0, 15))

        # Email (hidden by default)
        self.email_label = tk.Label(form_frame, text="Email:", bg=self.app.colors["text_light"])
        self.email_entry = tk.Entry(form_frame, font=("Arial", 11), width=35)

        # Phone (hidden by default)
        self.phone_label = tk.Label(form_frame, text="Phone:", bg=self.app.colors["text_light"])
        self.phone_entry = tk.Entry(form_frame, font=("Arial", 11), width=35)

        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.app.colors["text_light"])
        button_frame.pack(pady=20)

        self.submit_button = tk.Button(
            button_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"],
            width=15,
            command=self.handle_login
        )
        self.submit_button.pack(pady=5)

        # Toggle button
        self.toggle_button = tk.Button(
            button_frame,
            text="Register",
            font=("Arial", 11),
            bg=self.app.colors["bg_light"],
            fg=self.app.colors["accent"],
            width=15,
            command=self.toggle_form
        )
        self.toggle_button.pack(pady=5)

        # Message label
        self.message_label = tk.Label(
            form_frame,
            text="",
            font=("Arial", 10),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["danger"]
        )
        self.message_label.pack(pady=10)

        # Test credentials hint
        hint_frame = tk.Frame(form_frame, bg=self.app.colors["bg_light"])
        hint_frame.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(
            hint_frame,
            text="Test Login: testuser / test123",
            font=("Arial", 9),
            bg=self.app.colors["bg_light"],
            fg="#666666"
        ).pack()

    def toggle_form(self):
        """Toggle between login and register forms."""
        self.is_register = not self.is_register

        if self.is_register:
            self.title_label.config(text="Register")
            self.submit_button.config(text="Register")
            self.toggle_button.config(text="Back to Login")
            self.email_label.pack(anchor=tk.W, padx=30, pady=(10, 0))
            self.email_entry.pack(padx=30, pady=(0, 15))
            self.phone_label.pack(anchor=tk.W, padx=30, pady=(10, 0))
            self.phone_entry.pack(padx=30, pady=(0, 15))
        else:
            self.title_label.config(text="Login")
            self.submit_button.config(text="Login")
            self.toggle_button.config(text="Register")
            self.email_label.pack_forget()
            self.email_entry.pack_forget()
            self.phone_label.pack_forget()
            self.phone_entry.pack_forget()

        self.message_label.config(text="")

    def handle_login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            self.message_label.config(text="Please fill all fields")
            return

        if self.is_register:
            self.handle_register(username, password)
        else:
            self.authenticate_user(username, password)

    def authenticate_user(self, username: str, password: str):
        """Authenticate user login."""
        user = self.app.db.get_user_by_username(username)

        if not user:
            self.message_label.config(text="User not found")
            return

        if not PasswordManager.verify_password(password, user.get('password')):
            self.message_label.config(text="Incorrect password")
            return

        # Login successful
        self.app.current_user = username
        self.app.show_movie_listing()

    def handle_register(self, username: str, password: str):
        """Handle user registration."""
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # Validation
        if not Validator.is_valid_username(username):
            self.message_label.config(text="Username: 3-20 alphanumeric characters")
            return

        if not Validator.is_valid_password(password):
            self.message_label.config(text="Password must be at least 6 characters")
            return

        if not Validator.is_valid_email(email):
            self.message_label.config(text="Invalid email address")
            return

        if not Validator.validate_phone(phone):
            self.message_label.config(text="Phone must be 10 digits")
            return

        # Check if user exists
        if self.app.db.get_user_by_username(username):
            self.message_label.config(text="Username already exists")
            return

        # Create user
        user_data = {
            "username": username,
            "password": PasswordManager.hash_password(password),
            "email": email,
            "phone": phone,
            "registration_date": DateTimeHelper.get_current_date()
        }

        if self.app.db.add_user(user_data):
            self.message_label.config(text="Registration successful! Login now.", fg=self.app.colors["success"])
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.toggle_form()
        else:
            self.message_label.config(text="Registration failed")


class MovieListingScreen:
    """Movie listing and search screen."""

    def __init__(self, parent: tk.Frame, app: MovieBookingApp):
        """
        Initialize movie listing screen.

        Args:
            parent: Parent frame
            app: Main application instance
        """
        self.parent = parent
        self.app = app
        self.movies = self.app.db.get_movies()
        self.filtered_movies = self.movies.copy()

        # Main container
        container = tk.Frame(parent, bg=self.app.colors["bg_dark"])
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(container, bg=self.app.colors["accent"], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_label = tk.Label(
            header,
            text=f"Welcome, {self.app.current_user}! 🎬 Available Movies",
            font=("Arial", 18, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"]
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=20)

        button_frame = tk.Frame(header, bg=self.app.colors["accent"])
        button_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        tk.Button(
            button_frame,
            text="My Bookings",
            font=("Arial", 11, "bold"),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["accent"],
            command=self.app.show_booking_history
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Logout",
            font=("Arial", 11, "bold"),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["danger"],
            command=self.app.logout
        ).pack(side=tk.LEFT, padx=5)

        # Search and filter frame
        search_frame = tk.Frame(container, bg=self.app.colors["bg_light"], height=60)
        search_frame.pack(fill=tk.X)
        search_frame.pack_propagate(False)

        tk.Label(search_frame, text="Search:", bg=self.app.colors["bg_light"], font=("Arial", 11)).pack(side=tk.LEFT, padx=20, pady=10)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_movies())

        tk.Label(search_frame, text="Genre:", bg=self.app.colors["bg_light"], font=("Arial", 11)).pack(side=tk.LEFT, padx=(20, 5), pady=10)
        self.genre_var = tk.StringVar(value="All")
        self.genre_combo = ttk.Combobox(
            search_frame,
            textvariable=self.genre_var,
            font=("Arial", 11),
            width=15,
            state="readonly"
        )
        self.genre_combo.pack(side=tk.LEFT, padx=5, pady=10)
        self.genre_combo.bind("<<ComboboxSelected>>", lambda e: self.filter_movies())

        # Populate genres
        genres = set([m.get('genre') for m in self.movies])
        self.genre_combo['values'] = ["All"] + sorted(list(genres))

        # Movies frame with scrollbar
        movies_container = tk.Frame(container, bg=self.app.colors["bg_dark"])
        movies_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        canvas = tk.Canvas(movies_container, bg=self.app.colors["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(movies_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.app.colors["bg_dark"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add movies to scrollable frame
        self.movie_frames = {}
        for movie in self.filtered_movies:
            self.create_movie_card(scrollable_frame, movie)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = scrollable_frame
        self.canvas = canvas

    def create_movie_card(self, parent: tk.Frame, movie: dict):
        """Create a movie card widget."""
        card = tk.Frame(parent, bg=self.app.colors["text_light"], relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, pady=10)

        # Movie info
        info_frame = tk.Frame(card, bg=self.app.colors["text_light"])
        info_frame.pack(fill=tk.X, padx=15, pady=15)

        title = tk.Label(
            info_frame,
            text=movie['title'],
            font=("Arial", 14, "bold"),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["text_dark"]
        )
        title.pack(anchor=tk.W)

        details_text = f"{movie['genre']} • {movie['duration']} • {movie['rating']}"
        details = tk.Label(
            info_frame,
            text=details_text,
            font=("Arial", 10),
            bg=self.app.colors["text_light"],
            fg="#666666"
        )
        details.pack(anchor=tk.W, pady=(5, 10))

        description = tk.Label(
            info_frame,
            text=movie['description'],
            font=("Arial", 10),
            bg=self.app.colors["text_light"],
            fg="#555555",
            wraplength=500,
            justify=tk.LEFT
        )
        description.pack(anchor=tk.W, pady=(0, 10))

        # Book button
        book_button = tk.Button(
            info_frame,
            text="Book Tickets →",
            font=("Arial", 11, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"],
            command=lambda: self.app.show_seat_selection(movie['id'])
        )
        book_button.pack(anchor=tk.W, pady=(10, 0))

        self.movie_frames[movie['id']] = card

    def filter_movies(self):
        """Filter movies based on search and genre."""
        search_text = self.search_entry.get().strip().lower()
        selected_genre = self.genre_var.get()

        self.filtered_movies = []
        for movie in self.movies:
            # Check search
            if search_text and search_text not in movie['title'].lower():
                continue

            # Check genre
            if selected_genre != "All" and movie['genre'] != selected_genre:
                continue

            self.filtered_movies.append(movie)

        # Update display
        for mid, frame in self.movie_frames.items():
            if mid in [m['id'] for m in self.filtered_movies]:
                frame.pack(fill=tk.X, pady=10)
            else:
                frame.pack_forget()


class SeatSelectionScreen:
    """Seat selection screen."""

    def __init__(self, parent: tk.Frame, app: MovieBookingApp, movie_id: int):
        """
        Initialize seat selection screen.

        Args:
            parent: Parent frame
            app: Main application instance
            movie_id: Selected movie ID
        """
        self.parent = parent
        self.app = app
        self.movie_id = movie_id
        self.movie = app.db.get_movie_by_id(movie_id)
        self.selected_seats = []
        self.selected_showtime = None

        # Main container
        container = tk.Frame(parent, bg=self.app.colors["bg_dark"])
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(container, bg=self.app.colors["accent"], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_label = tk.Label(
            header,
            text=f"← Select Seats for {self.movie['title']}",
            font=("Arial", 16, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"]
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=15)

        back_button = tk.Button(
            header,
            text="← Back",
            font=("Arial", 11, "bold"),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["accent"],
            command=self.app.show_movie_listing
        )
        back_button.pack(side=tk.RIGHT, padx=20, pady=15)

        # Content
        content = tk.Frame(container, bg=self.app.colors["bg_light"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Showtime selection
        showtime_frame = tk.Frame(content, bg=self.app.colors["bg_light"])
        showtime_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(showtime_frame, text="Select Showtime:", font=("Arial", 12, "bold"), bg=self.app.colors["bg_light"]).pack(anchor=tk.W)

        self.showtime_var = tk.StringVar()
        for showtime in self.movie['showtimes']:
            tk.Radiobutton(
                showtime_frame,
                text=showtime,
                variable=self.showtime_var,
                value=showtime,
                font=("Arial", 11),
                bg=self.app.colors["bg_light"],
                command=self.on_showtime_selected
            ).pack(anchor=tk.W, pady=2)

        # Seat information
        info_frame = tk.Frame(content, bg=self.app.colors["text_light"], relief=tk.SUNKEN, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(info_frame, text="●", font=("Arial", 14), fg="green", bg=self.app.colors["text_light"]).pack(side=tk.LEFT, padx=10)
        tk.Label(info_frame, text="Available", font=("Arial", 11), bg=self.app.colors["text_light"]).pack(side=tk.LEFT, padx=5)

        tk.Label(info_frame, text="●", font=("Arial", 14), fg="red", bg=self.app.colors["text_light"]).pack(side=tk.LEFT, padx=10)
        tk.Label(info_frame, text="Booked", font=("Arial", 11), bg=self.app.colors["text_light"]).pack(side=tk.LEFT, padx=5)

        tk.Label(info_frame, text="●", font=("Arial", 14), fg="gold", bg=self.app.colors["text_light"]).pack(side=tk.LEFT, padx=10)
        tk.Label(info_frame, text="Selected", font=("Arial", 11), bg=self.app.colors["text_light"]).pack(side=tk.LEFT, padx=5)

        tk.Label(info_frame, text="", bg=self.app.colors["text_light"]).pack(side=tk.LEFT, padx=10)

        # Seat grid
        self.seats_frame = tk.Frame(content, bg=self.app.colors["bg_light"])
        self.seats_frame.pack(pady=20)

        self.seat_buttons = {}
        self.create_seat_grid()

        # Selection summary
        summary_frame = tk.Frame(content, bg=self.app.colors["text_light"], relief=tk.SUNKEN, bd=1)
        summary_frame.pack(fill=tk.X, pady=(20, 0))

        self.summary_label = tk.Label(
            summary_frame,
            text="Selected Seats: None | Total: ₹0",
            font=("Arial", 12),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["text_dark"]
        )
        self.summary_label.pack(pady=10)

        # Proceed button
        self.proceed_button = tk.Button(
            content,
            text="Proceed to Booking",
            font=("Arial", 12, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"],
            state=tk.DISABLED,
            command=self.proceed_to_booking
        )
        self.proceed_button.pack(pady=20)

    def create_seat_grid(self):
        """Create the seat selection grid."""
        # Clear existing buttons
        for widget in self.seats_frame.winfo_children():
            widget.destroy()
        self.seat_buttons.clear()

        rows = 10
        cols = 15
        row_labels = [chr(65 + i) for i in range(rows)]

        # Column headers
        header_frame = tk.Frame(self.seats_frame, bg=self.app.colors["bg_light"])
        header_frame.pack()

        tk.Label(header_frame, text="  ", bg=self.app.colors["bg_light"]).grid(row=0, column=0, padx=2, pady=2)
        for col in range(1, cols + 1):
            tk.Label(header_frame, text=str(col), font=("Arial", 8), bg=self.app.colors["bg_light"], width=3).grid(row=0, column=col, padx=2, pady=2)

        # Seat grid
        for row_idx, row_label in enumerate(row_labels, 1):
            tk.Label(header_frame, text=row_label, font=("Arial", 9, "bold"), bg=self.app.colors["bg_light"]).grid(row=row_idx, column=0, padx=2, pady=2)

            for col in range(1, cols + 1):
                seat_id = f"{row_label}{col}"
                btn = tk.Button(
                    header_frame,
                    text="●",
                    font=("Arial", 12),
                    width=3,
                    height=1,
                    bg="green",
                    fg="green",
                    activebackground="lightgreen",
                    command=lambda s=seat_id: self.toggle_seat(s)
                )
                btn.grid(row=row_idx, column=col, padx=2, pady=2)
                self.seat_buttons[seat_id] = btn

    def on_showtime_selected(self):
        """Handle showtime selection."""
        self.selected_showtime = self.showtime_var.get()
        self.update_seat_availability()

    def update_seat_availability(self):
        """Update seat availability based on selected showtime."""
        if not self.selected_showtime:
            return

        booked_seats = self.app.booking_manager.get_booked_seats(self.movie_id, self.selected_showtime)

        for seat_id, btn in self.seat_buttons.items():
            if seat_id in booked_seats:
                btn.config(state=tk.DISABLED, bg="red", fg="red", activebackground="red")
            elif seat_id in self.selected_seats:
                btn.config(state=tk.NORMAL, bg="gold", fg="gold", activebackground="yellow")
            else:
                btn.config(state=tk.NORMAL, bg="green", fg="green", activebackground="lightgreen")

    def toggle_seat(self, seat_id: str):
        """Toggle seat selection."""
        if not self.selected_showtime:
            messagebox.showwarning("Warning", "Please select a showtime first")
            return

        if seat_id in self.selected_seats:
            self.selected_seats.remove(seat_id)
        else:
            if len(self.selected_seats) >= 10:
                messagebox.showwarning("Limit", "Cannot book more than 10 seats")
                return
            self.selected_seats.append(seat_id)

        # Sort seats
        self.selected_seats.sort()

        # Update UI
        self.update_seat_availability()
        self.update_summary()

    def update_summary(self):
        """Update the selection summary label."""
        if self.selected_seats:
            seats_str = ", ".join(self.selected_seats)
            total_cost = PriceCalculator.calculate_total(len(self.selected_seats), self.selected_showtime)
            self.summary_label.config(
                text=f"Selected Seats: {seats_str} | Total: ₹{total_cost}"
            )
            self.proceed_button.config(state=tk.NORMAL)
        else:
            self.summary_label.config(text="Selected Seats: None | Total: ₹0")
            self.proceed_button.config(state=tk.DISABLED)

    def proceed_to_booking(self):
        """Proceed to booking confirmation."""
        self.app.show_booking_confirmation(self.movie_id, self.selected_seats, self.selected_showtime)


class BookingConfirmationScreen:
    """Booking confirmation and payment screen."""

    def __init__(self, parent: tk.Frame, app: MovieBookingApp, movie_id: int, seats: List[str], show_time: str):
        """
        Initialize booking confirmation screen.

        Args:
            parent: Parent frame
            app: Main application instance
            movie_id: Movie ID
            seats: Selected seats
            show_time: Selected showtime
        """
        self.parent = parent
        self.app = app
        self.movie_id = movie_id
        self.movie = app.db.get_movie_by_id(movie_id)
        self.seats = seats
        self.show_time = show_time
        self.user = app.db.get_user_by_username(app.current_user)

        # Main container
        container = tk.Frame(parent, bg=self.app.colors["bg_light"])
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(container, bg=self.app.colors["accent"], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_label = tk.Label(
            header,
            text="← Confirm Your Booking",
            font=("Arial", 16, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"]
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=15)

        back_button = tk.Button(
            header,
            text="← Back",
            font=("Arial", 11, "bold"),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["accent"],
            command=lambda: self.app.show_seat_selection(movie_id)
        )
        back_button.pack(side=tk.RIGHT, padx=20, pady=15)

        # Content
        content = tk.Frame(container, bg=self.app.colors["bg_light"])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Booking details
        self.create_booking_details(content)

    def create_booking_details(self, parent: tk.Frame):
        """Create booking details display."""
        # Movie details section
        details_frame = tk.Frame(parent, bg=self.app.colors["text_light"], relief=tk.SUNKEN, bd=1)
        details_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            details_frame,
            text="BOOKING DETAILS",
            font=("Arial", 14, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"]
        ).pack(fill=tk.X, padx=15, pady=10)

        info = tk.Frame(details_frame, bg=self.app.colors["text_light"])
        info.pack(fill=tk.X, padx=15, pady=10)

        self.create_detail_row(info, "Movie:", self.movie['title'])
        self.create_detail_row(info, "Genre:", self.movie['genre'])
        self.create_detail_row(info, "Showtime:", self.show_time)
        self.create_detail_row(info, "Seats:", ", ".join(self.seats))
        self.create_detail_row(info, "Number of Tickets:", str(len(self.seats)))

        total_cost = PriceCalculator.calculate_total(len(self.seats), self.show_time)
        self.create_detail_row(info, "Cost per Ticket:", f"₹{PriceCalculator.get_cost_per_seat(self.show_time)}", bold=True)
        self.create_detail_row(info, "Total Amount:", f"₹{total_cost}", bold=True)

        # User info section
        user_frame = tk.Frame(parent, bg=self.app.colors["text_light"], relief=tk.SUNKEN, bd=1)
        user_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            user_frame,
            text="PASSENGER DETAILS",
            font=("Arial", 14, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"]
        ).pack(fill=tk.X, padx=15, pady=10)

        info2 = tk.Frame(user_frame, bg=self.app.colors["text_light"])
        info2.pack(fill=tk.X, padx=15, pady=10)

        self.create_detail_row(info2, "Name:", self.app.current_user)
        self.create_detail_row(info2, "Email:", self.user.get('email'))
        self.create_detail_row(info2, "Phone:", self.user.get('phone'))

        # Confirmation buttons
        button_frame = tk.Frame(parent, bg=self.app.colors["bg_light"])
        button_frame.pack(fill=tk.X, pady=20)

        tk.Button(
            button_frame,
            text="Confirm Booking",
            font=("Arial", 12, "bold"),
            bg=self.app.colors["success"],
            fg=self.app.colors["text_light"],
            width=25,
            command=self.confirm_booking
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 12, "bold"),
            bg=self.app.colors["danger"],
            fg=self.app.colors["text_light"],
            width=25,
            command=lambda: self.app.show_seat_selection(self.movie_id)
        ).pack(side=tk.LEFT, padx=10)

    def create_detail_row(self, parent: tk.Frame, label: str, value: str, bold: bool = False):
        """Create a detail row in the booking details."""
        row = tk.Frame(parent, bg=self.app.colors["text_light"])
        row.pack(fill=tk.X, pady=5)

        label_font = ("Arial", 11, "bold") if bold else ("Arial", 11)
        value_font = ("Arial", 11, "bold") if bold else ("Arial", 11)

        tk.Label(row, text=label, font=label_font, bg=self.app.colors["text_light"]).pack(side=tk.LEFT, width=20)
        tk.Label(row, text=value, font=value_font, bg=self.app.colors["text_light"], fg=self.app.colors["accent"]).pack(side=tk.LEFT)

    def confirm_booking(self):
        """Confirm and process the booking."""
        result = self.app.booking_manager.create_booking(
            username=self.app.current_user,
            movie_id=self.movie_id,
            show_time=self.show_time,
            selected_seats=self.seats,
            email=self.user.get('email'),
            phone=self.user.get('phone')
        )

        if result['success']:
            # Show success message
            booking = result['booking']
            messagebox.showinfo(
                "Booking Confirmed",
                f"Booking ID: {booking['booking_id']}\n\n"
                f"Movie: {booking['movie_title']}\n"
                f"Seats: {', '.join(booking['seats'])}\n"
                f"Total: ₹{booking['total_cost']}\n\n"
                "Your tickets have been booked successfully!"
            )
            self.app.show_movie_listing()
        else:
            messagebox.showerror("Booking Failed", result['message'])


class BookingHistoryScreen:
    """User booking history screen."""

    def __init__(self, parent: tk.Frame, app: MovieBookingApp):
        """
        Initialize booking history screen.

        Args:
            parent: Parent frame
            app: Main application instance
        """
        self.parent = parent
        self.app = app
        self.bookings = app.booking_manager.get_user_bookings(app.current_user)

        # Main container
        container = tk.Frame(parent, bg=self.app.colors["bg_light"])
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(container, bg=self.app.colors["accent"], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_label = tk.Label(
            header,
            text="← My Bookings",
            font=("Arial", 16, "bold"),
            bg=self.app.colors["accent"],
            fg=self.app.colors["text_light"]
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=15)

        back_button = tk.Button(
            header,
            text="← Back",
            font=("Arial", 11, "bold"),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["accent"],
            command=self.app.show_movie_listing
        )
        back_button.pack(side=tk.RIGHT, padx=20, pady=15)

        # Content
        content = tk.Frame(container, bg=self.app.colors["bg_light"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        if not self.bookings:
            empty_label = tk.Label(
                content,
                text="No bookings yet. Book your first movie!",
                font=("Arial", 14),
                bg=self.app.colors["bg_light"],
                fg="#999999"
            )
            empty_label.pack(expand=True)
        else:
            # Show bookings
            canvas = tk.Canvas(content, bg=self.app.colors["bg_light"], highlightthickness=0)
            scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.app.colors["bg_light"])

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            for booking in self.bookings:
                self.create_booking_card(scrollable_frame, booking)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

    def create_booking_card(self, parent: tk.Frame, booking: dict):
        """Create a booking card."""
        card = tk.Frame(parent, bg=self.app.colors["text_light"], relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, pady=10)

        info = tk.Frame(card, bg=self.app.colors["text_light"])
        info.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            info,
            text=f"Booking ID: {booking['booking_id']}",
            font=("Arial", 12, "bold"),
            bg=self.app.colors["text_light"],
            fg=self.app.colors["accent"]
        ).pack(anchor=tk.W)

        details = f"{booking['movie_title']} • {booking['show_time']}"
        tk.Label(info, text=details, font=("Arial", 11), bg=self.app.colors["text_light"]).pack(anchor=tk.W, pady=(5, 0))

        seats = f"Seats: {', '.join(booking['seats'])}"
        tk.Label(info, text=seats, font=("Arial", 10), bg=self.app.colors["text_light"], fg="#666666").pack(anchor=tk.W)

        amount = f"Amount Paid: ₹{booking['total_cost']}"
        tk.Label(info, text=amount, font=("Arial", 11, "bold"), bg=self.app.colors["text_light"], fg=self.app.colors["success"]).pack(anchor=tk.W, pady=(5, 0))
