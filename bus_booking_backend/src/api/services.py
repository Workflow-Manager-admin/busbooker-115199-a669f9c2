import hashlib
import uuid
from datetime import datetime
from typing import List, Dict, Optional

from .models import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    BusSearchRequest,
    BusInfo,
    SeatInfo,
    BookingRequest,
    BookingResponse,
    BookingHistoryResponse,
    PaymentRequest,
    TicketResponse,
)


# In-memory stores for demonstration. In production, use a real database.
users_db: Dict[str, dict] = {}
buses_db: Dict[int, dict] = {}
bookings_db: Dict[int, dict] = {}
seats_db: Dict[int, Dict[str, bool]] = {}


# Simulate buses on various routes
def _populate_buses():
    buses_db.clear()
    seats_db.clear()
    now = datetime.now()
    buses = [
        {
            "bus_id": 1,
            "operator": "Blue Line",
            "origin": "New York",
            "destination": "Boston",
            "departure_time": now.replace(
                hour=9, minute=0, second=0, microsecond=0
            ),
            "arrival_time": now.replace(
                hour=13, minute=0, second=0, microsecond=0
            ),
            "total_seats": 40,
            "fare": 25.0,
        },
        {
            "bus_id": 2,
            "operator": "Red Express",
            "origin": "New York",
            "destination": "Washington",
            "departure_time": now.replace(
                hour=10, minute=0, second=0, microsecond=0
            ),
            "arrival_time": now.replace(
                hour=14, minute=0, second=0, microsecond=0
            ),
            "total_seats": 40,
            "fare": 30.0,
        },
        {
            "bus_id": 3,
            "operator": "Metro Travels",
            "origin": "Boston",
            "destination": "New York",
            "departure_time": now.replace(
                hour=16, minute=0, second=0, microsecond=0
            ),
            "arrival_time": now.replace(
                hour=20, minute=0, second=0, microsecond=0
            ),
            "total_seats": 40,
            "fare": 27.5,
        },
    ]
    for bus in buses:
        bus_id = bus["bus_id"]
        buses_db[bus_id] = bus
        # All seats available at start
        seats_db[bus_id] = {f"{i + 1:02d}A": True for i in range(bus["total_seats"])}


# Simple hashing for demo only
def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# PUBLIC_INTERFACE
def register_user(payload: UserRegisterRequest) -> UserResponse:
    """Register a new user."""
    if payload.username in users_db or any(
        u["email"] == payload.email for u in users_db.values()
    ):
        raise ValueError("User already exists")
    user_id = len(users_db) + 1
    users_db[payload.username] = {
        "id": user_id,
        "username": payload.username,
        "email": payload.email,
        "password_hash": _hash_password(payload.password),
    }
    return UserResponse(id=user_id, username=payload.username, email=payload.email)


# PUBLIC_INTERFACE
def authenticate_user(payload: UserLoginRequest) -> Optional[UserResponse]:
    """Authenticate a user; returns UserResponse if credentials are valid."""
    user = users_db.get(payload.username)
    if not user:
        return None
    if user["password_hash"] != _hash_password(payload.password):
        return None
    return UserResponse(
        id=user["id"], username=user["username"], email=user["email"]
    )


# PUBLIC_INTERFACE
def generate_jwt_token(user: UserResponse) -> str:
    """Mock token generator."""
    # In production, use JWT library and secret key
    return f"TOKEN-{user.id}-{uuid.uuid4().hex}"


# PUBLIC_INTERFACE
def search_buses(payload: BusSearchRequest) -> List[BusInfo]:
    """Search buses by origin, destination, and travel date."""
    results = []
    for bus in buses_db.values():
        if (
            bus["origin"].lower() == payload.origin.lower()
            and bus["destination"].lower() == payload.destination.lower()
        ):
            taken = [
                seat
                for booking in bookings_db.values()
                if booking["bus_id"] == bus["bus_id"]
                and booking["travel_date"] == payload.travel_date
                for seat in booking["seat_numbers"]
            ]
            available = bus["total_seats"] - len(taken)
            results.append(
                BusInfo(
                    bus_id=bus["bus_id"],
                    operator=bus["operator"],
                    origin=bus["origin"],
                    destination=bus["destination"],
                    departure_time=bus["departure_time"],
                    arrival_time=bus["arrival_time"],
                    total_seats=bus["total_seats"],
                    available_seats=available,
                    fare=bus["fare"],
                )
            )
    return results


# PUBLIC_INTERFACE
def get_seat_map(bus_id: int, travel_date) -> List[SeatInfo]:
    """Fetch seat map for a given bus and travel date."""
    bus = buses_db.get(bus_id)
    if not bus:
        raise ValueError("Bus not found")
    # All seats available by default; mark booked ones
    seat_list = [
        SeatInfo(seat_number=s, is_available=True) for s in seats_db[bus_id].keys()
    ]
    for booking in bookings_db.values():
        if booking["bus_id"] == bus_id and booking["travel_date"] == travel_date:
            booked_seats = booking["seat_numbers"]
            for seat in seat_list:
                if seat.seat_number in booked_seats:
                    seat.is_available = False
    return seat_list


# PUBLIC_INTERFACE
def book_tickets(user_id: int, payload: BookingRequest) -> BookingResponse:
    """Book ticket(s) for a user."""
    bus = buses_db.get(payload.bus_id)
    if not bus:
        raise ValueError("Bus not found")
    travel_date = payload.travel_date
    seat_map = get_seat_map(payload.bus_id, travel_date)
    available_seats = {s.seat_number for s in seat_map if s.is_available}
    for seat in payload.seat_numbers:
        if seat not in available_seats:
            raise ValueError(f"Seat {seat} is not available")
    booking_id = len(bookings_db) + 1
    bookings_db[booking_id] = {
        "booking_id": booking_id,
        "user_id": user_id,
        "bus_id": payload.bus_id,
        "travel_date": travel_date,
        "seat_numbers": payload.seat_numbers,
        "passenger_names": payload.passenger_names,
        "status": "CONFIRMED",
        "payment_status": "PENDING",
        "booking_date": datetime.now(),
    }
    return BookingResponse(
        booking_id=booking_id,
        user_id=user_id,
        bus_id=payload.bus_id,
        seat_numbers=payload.seat_numbers,
        status="CONFIRMED",
        payment_status="PENDING",
        ticket_url=None,
    )


# PUBLIC_INTERFACE
def process_payment(user_id: int, payload: PaymentRequest) -> BookingResponse:
    """Process payment for a booking."""
    booking = bookings_db.get(payload.booking_id)
    if not booking:
        raise ValueError("Booking not found")
    if booking["user_id"] != user_id:
        raise ValueError("Unauthorized")
    # Simulate payment success
    booking["payment_status"] = "SUCCESS"
    return BookingResponse(
        booking_id=booking["booking_id"],
        user_id=booking["user_id"],
        bus_id=booking["bus_id"],
        seat_numbers=booking["seat_numbers"],
        status=booking["status"],
        payment_status="SUCCESS",
        ticket_url=f"/tickets/{booking['booking_id']}",
    )


# PUBLIC_INTERFACE
def get_ticket(user_id: int, booking_id: int) -> TicketResponse:
    """Get ticket details/download link."""
    booking = bookings_db.get(booking_id)
    if not booking or booking["user_id"] != user_id:
        raise ValueError("Booking not found")
    return TicketResponse(
        booking_id=booking_id,
        ticket_url=f"/tickets/{booking_id}",
        seat_numbers=booking["seat_numbers"],
    )


# PUBLIC_INTERFACE
def get_booking_history(user_id: int) -> List[BookingHistoryResponse]:
    """Return booking history for a user."""
    items = []
    for booking in bookings_db.values():
        if booking["user_id"] == user_id:
            bus = buses_db[booking["bus_id"]]
            items.append(
                BookingHistoryResponse(
                    booking_id=booking["booking_id"],
                    bus_info=BusInfo(
                        bus_id=bus["bus_id"],
                        operator=bus["operator"],
                        origin=bus["origin"],
                        destination=bus["destination"],
                        departure_time=bus["departure_time"],
                        arrival_time=bus["arrival_time"],
                        total_seats=bus["total_seats"],
                        available_seats=bus["total_seats"],  # Not reflecting (historic only)
                        fare=bus["fare"],
                    ),
                    seat_numbers=booking["seat_numbers"],
                    booking_date=booking["booking_date"],
                    travel_date=booking["travel_date"],
                    status=booking["status"],
                    payment_status=booking["payment_status"],
                )
            )
    return items


# Call on module import to populate buses
_populate_buses()
