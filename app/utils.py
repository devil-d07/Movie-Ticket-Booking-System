"""
Utility functions for the movie booking application.
Includes validation, password hashing, and other helper functions.
"""

import hashlib
import re
from datetime import datetime
from typing import Tuple

class Validator:
    """Email and input validation utilities."""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_username(username: str) -> bool:
        """
        Validate username (3-20 alphanumeric characters, underscores allowed).

        Args:
            username: Username to validate

        Returns:
            True if valid, False otherwise
        """
        if len(username) < 3 or len(username) > 20:
            return False
        pattern = r'^[a-zA-Z0-9_]+$'
        return re.match(pattern, username) is not None

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Validate password (minimum 6 characters).

        Args:
            password: Password to validate

        Returns:
            True if valid, False otherwise
        """
        return len(password) >= 6

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number (10 digits).

        Args:
            phone: Phone number to validate

        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[0-9]{10}$'
        return re.match(pattern, phone) is not None


class PasswordManager:
    """Handle password hashing and verification."""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using SHA-256.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            password: Plain text password
            hashed: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        return PasswordManager.hash_password(password) == hashed


class SeatHelper:
    """Helper functions for seat management."""

    @staticmethod
    def generate_seats(rows: int = 10, cols: int = 15) -> dict:
        """
        Generate a seat layout grid.

        Args:
            rows: Number of rows (A-Z)
            cols: Number of columns (1-based)

        Returns:
            Dictionary with seat positions and availability
        """
        seats = {}
        row_labels = [chr(65 + i) for i in range(rows)]

        for row in row_labels:
            for col in range(1, cols + 1):
                seat_id = f"{row}{col}"
                seats[seat_id] = {
                    "available": True,
                    "booked": False,
                    "selected": False
                }

        return seats

    @staticmethod
    def get_seat_coordinates(seat_id: str) -> Tuple[str, int]:
        """
        Parse seat ID to get row and column.

        Args:
            seat_id: Seat identifier (e.g., 'A1')

        Returns:
            Tuple of (row, column)
        """
        row = seat_id[0]
        col = int(seat_id[1:])
        return row, col

    @staticmethod
    def is_valid_seat(seat_id: str) -> bool:
        """
        Validate seat ID format.

        Args:
            seat_id: Seat identifier

        Returns:
            True if valid, False otherwise
        """
        if len(seat_id) < 2:
            return False
        row = seat_id[0]
        try:
            col = int(seat_id[1:])
            return ord(row) >= 65 and col >= 1
        except ValueError:
            return False


class PriceCalculator:
    """Calculate ticket prices."""

    BASE_PRICE = 250  # Base ticket price in currency units

    @staticmethod
    def get_cost_per_seat(show_time: str = "standard") -> int:
        """
        Get price per seat based on show time.

        Args:
            show_time: Show time (e.g., "10:00 AM", "8:30 PM")

        Returns:
            Price per seat
        """
        hour = int(show_time.split(':')[0])

        # Peak hours (evening shows): 7 PM - 10 PM
        if 19 <= hour <= 22:
            return int(PriceCalculator.BASE_PRICE * 1.3)

        # Regular hours
        return PriceCalculator.BASE_PRICE

    @staticmethod
    def calculate_total(num_seats: int, show_time: str = "standard") -> int:
        """
        Calculate total booking cost.

        Args:
            num_seats: Number of seats
            show_time: Show time

        Returns:
            Total cost
        """
        cost_per_seat = PriceCalculator.get_cost_per_seat(show_time)
        return num_seats * cost_per_seat


class DateTimeHelper:
    """Date and time utility functions."""

    @staticmethod
    def get_current_datetime() -> str:
        """Get current date and time as formatted string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_date() -> str:
        """Get current date as formatted string."""
        return datetime.now().strftime("%Y-%m-%d")
