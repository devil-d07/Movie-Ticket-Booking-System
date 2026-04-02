"""
Booking module for handling booking operations.
Manages seat selection, booking creation, and booking history.
"""

from datetime import datetime
from typing import List, Dict, Optional
from app.database import Database
from app.utils import SeatHelper, PriceCalculator, DateTimeHelper


class BookingManager:
    """Manages all booking operations."""

    def __init__(self, database: Database):
        """
        Initialize BookingManager.

        Args:
            database: Database instance for data persistence
        """
        self.db = database
        self.current_booking = {}
        self.selected_seats = []

    def create_booking(
        self,
        username: str,
        movie_id: int,
        show_time: str,
        selected_seats: List[str],
        email: str,
        phone: str
    ) -> Dict:
        """
        Create a new booking.

        Args:
            username: Username of the customer
            movie_id: ID of the movie
            show_time: Selected show time
            selected_seats: List of selected seat IDs
            email: Customer email
            phone: Customer phone number

        Returns:
            Booking dictionary with booking details
        """
        movie = self.db.get_movie_by_id(movie_id)

        if not movie:
            return {"success": False, "message": "Movie not found"}

        # Validate seats
        if not selected_seats or len(selected_seats) == 0:
            return {"success": False, "message": "No seats selected"}

        if len(selected_seats) > 10:
            return {"success": False, "message": "Cannot book more than 10 seats"}

        # Calculate price
        total_cost = PriceCalculator.calculate_total(len(selected_seats), show_time)

        # Create booking record
        booking = {
            "booking_id": self._generate_booking_id(),
            "username": username,
            "movie_id": movie_id,
            "movie_title": movie.get('title'),
            "genre": movie.get('genre'),
            "show_time": show_time,
            "seats": selected_seats,
            "num_seats": len(selected_seats),
            "total_cost": total_cost,
            "email": email,
            "phone": phone,
            "booking_date": DateTimeHelper.get_current_date(),
            "booking_time": DateTimeHelper.get_current_datetime(),
            "status": "confirmed"
        }

        # Save booking
        if self.db.add_booking(booking):
            return {
                "success": True,
                "message": "Booking confirmed successfully",
                "booking": booking
            }
        else:
            return {"success": False, "message": "Failed to save booking"}

    def get_user_bookings(self, username: str) -> List[Dict]:
        """
        Get all bookings for a user.

        Args:
            username: Username

        Returns:
            List of bookings for the user
        """
        return self.db.get_bookings_by_user(username)

    def validate_seats(self, selected_seats: List[str]) -> bool:
        """
        Validate that all selected seats are valid.

        Args:
            selected_seats: List of seat IDs

        Returns:
            True if all seats are valid, False otherwise
        """
        for seat in selected_seats:
            if not SeatHelper.is_valid_seat(seat):
                return False
        return True

    def check_seat_availability(
        self,
        movie_id: int,
        show_time: str,
        seat_id: str
    ) -> bool:
        """
        Check if a specific seat is available for booking.

        Args:
            movie_id: Movie ID
            show_time: Show time
            seat_id: Seat ID

        Returns:
            True if available, False otherwise
        """
        bookings = self.db.get_bookings()

        for booking in bookings:
            if (booking.get('movie_id') == movie_id and
                booking.get('show_time') == show_time and
                seat_id in booking.get('seats', [])):
                return False

        return True

    def get_booked_seats(
        self,
        movie_id: int,
        show_time: str
    ) -> List[str]:
        """
        Get all booked seats for a specific movie and show time.

        Args:
            movie_id: Movie ID
            show_time: Show time

        Returns:
            List of booked seat IDs
        """
        bookings = self.db.get_bookings()
        booked_seats = []

        for booking in bookings:
            if (booking.get('movie_id') == movie_id and
                booking.get('show_time') == show_time):
                booked_seats.extend(booking.get('seats', []))

        return booked_seats

    def cancel_booking(self, booking_id: str) -> Dict:
        """
        Cancel a booking.

        Args:
            booking_id: Booking ID to cancel

        Returns:
            Status dictionary
        """
        bookings = self.db.get_bookings()

        for i, booking in enumerate(bookings):
            if booking.get('booking_id') == booking_id:
                bookings.pop(i)
                if self.db.save_bookings(bookings):
                    return {
                        "success": True,
                        "message": "Booking cancelled successfully"
                    }
                else:
                    return {
                        "success": False,
                        "message": "Failed to cancel booking"
                    }

        return {
            "success": False,
            "message": "Booking not found"
        }

    @staticmethod
    def _generate_booking_id() -> str:
        """
        Generate a unique booking ID.

        Returns:
            Booking ID string
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BK{timestamp}"
