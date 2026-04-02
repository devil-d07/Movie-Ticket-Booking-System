"""
Main entry point for the Movie Ticket Booking Application.
Run this file to start the application: python main.py
"""

import tkinter as tk
from app.gui import MovieBookingApp


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = MovieBookingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
