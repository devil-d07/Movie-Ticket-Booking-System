"""
Database module for handling JSON file operations.
Provides functions to read and write data to JSON files.
"""

import json
import os
from pathlib import Path
from typing import Any, List, Dict

class Database:
    """Handles all database operations with JSON files."""

    def __init__(self, data_dir: str = "data"):
        """
        Initialize Database with data directory.

        Args:
            data_dir: Directory path where JSON files are stored
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def load_json(self, filename: str) -> Any:
        """
        Load data from a JSON file.

        Args:
            filename: Name of the JSON file (without path)

        Returns:
            Parsed JSON data or empty list/dict if file doesn't exist
        """
        filepath = self.data_dir / filename

        if not filepath.exists():
            return [] if filename.endswith('s.json') else {}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {filename}: {e}")
            return [] if filename.endswith('s.json') else {}

    def save_json(self, filename: str, data: Any) -> bool:
        """
        Save data to a JSON file.

        Args:
            filename: Name of the JSON file (without path)
            data: Data to save

        Returns:
            True if successful, False otherwise
        """
        filepath = self.data_dir / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error writing to {filename}: {e}")
            return False

    def get_movies(self) -> List[Dict]:
        """Load all movies from movies.json."""
        return self.load_json('movies.json')

    def get_users(self) -> List[Dict]:
        """Load all users from users.json."""
        return self.load_json('users.json')

    def get_bookings(self) -> List[Dict]:
        """Load all bookings from bookings.json."""
        return self.load_json('bookings.json')

    def save_users(self, users: List[Dict]) -> bool:
        """Save users to users.json."""
        return self.save_json('users.json', users)

    def save_bookings(self, bookings: List[Dict]) -> bool:
        """Save bookings to bookings.json."""
        return self.save_json('bookings.json', bookings)

    def get_movie_by_id(self, movie_id: int) -> Dict:
        """
        Get a specific movie by ID.

        Args:
            movie_id: Movie ID

        Returns:
            Movie dictionary or empty dict if not found
        """
        movies = self.get_movies()
        for movie in movies:
            if movie.get('id') == movie_id:
                return movie
        return {}

    def get_user_by_username(self, username: str) -> Dict:
        """
        Get a specific user by username.

        Args:
            username: User's username

        Returns:
            User dictionary or empty dict if not found
        """
        users = self.get_users()
        for user in users:
            if user.get('username') == username:
                return user
        return {}

    def get_bookings_by_user(self, username: str) -> List[Dict]:
        """
        Get all bookings for a specific user.

        Args:
            username: User's username

        Returns:
            List of bookings for the user
        """
        bookings = self.get_bookings()
        return [b for b in bookings if b.get('username') == username]

    def add_user(self, user_data: Dict) -> bool:
        """Add a new user to users.json."""
        users = self.get_users()
        users.append(user_data)
        return self.save_users(users)

    def add_booking(self, booking_data: Dict) -> bool:
        """Add a new booking to bookings.json."""
        bookings = self.get_bookings()
        bookings.append(booking_data)
        return self.save_bookings(bookings)
