from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


# PUBLIC_INTERFACE
class UserRegisterRequest(BaseModel):
    """Request payload for user registration."""

    username: str = Field(..., description="Unique username")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


# PUBLIC_INTERFACE
class UserLoginRequest(BaseModel):
    """Request payload for user login."""

    username: str = Field(..., description="Unique username")
    password: str = Field(..., description="User password")


# PUBLIC_INTERFACE
class UserResponse(BaseModel):
    """User response model."""

    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Unique username")
    email: EmailStr = Field(..., description="User email address")


# PUBLIC_INTERFACE
class TokenResponse(BaseModel):
    """Authentication token response."""

    access_token: str = Field(..., description="JWT Access token")
    token_type: str = Field(..., description="Token type (usually Bearer)")


# PUBLIC_INTERFACE
class BusSearchRequest(BaseModel):
    """Bus search filter."""

    origin: str = Field(..., description="Origin city")
    destination: str = Field(..., description="Destination city")
    travel_date: date = Field(..., description="Desired travel date")


# PUBLIC_INTERFACE
class BusInfo(BaseModel):
    """Response object for bus listing/search results."""

    bus_id: int = Field(..., description="Bus unique identifier")
    operator: str = Field(..., description="Bus operator name")
    origin: str = Field(..., description="Origin city")
    destination: str = Field(..., description="Destination city")
    departure_time: datetime = Field(..., description="Departure time")
    arrival_time: datetime = Field(..., description="Arrival time")
    total_seats: int = Field(..., description="Total seats on the bus")
    available_seats: int = Field(..., description="Number of available seats")
    fare: float = Field(..., description="Ticket fare")


# PUBLIC_INTERFACE
class SeatInfo(BaseModel):
    """Seat detail/info."""

    seat_number: str = Field(..., description="Seat identifier")
    is_available: bool = Field(..., description="Seat availability status")
    is_selected: Optional[bool] = Field(
        default=False,
        description="Currently selected by user"
    )


# PUBLIC_INTERFACE
class BookingRequest(BaseModel):
    """Request to create a booking."""

    bus_id: int = Field(..., description="Bus ID")
    travel_date: date = Field(..., description="Desired date of travel")
    seat_numbers: List[str] = Field(
        ..., description="List of seat numbers to book"
    )
    passenger_names: List[str] = Field(
        ..., description="Passenger's names for the tickets"
    )
    payment_method: str = Field(
        ..., description="Payment method, e.g., 'card', 'wallet', etc."
    )


# PUBLIC_INTERFACE
class BookingResponse(BaseModel):
    """Booking response."""

    booking_id: int = Field(..., description="Booking unique ID")
    user_id: int = Field(..., description="User who made the booking")
    bus_id: int = Field(..., description="Bus ID")
    seat_numbers: List[str] = Field(..., description="Booked seat numbers")
    status: str = Field(..., description="Booking status")
    payment_status: str = Field(..., description="Payment processing status")
    ticket_url: Optional[str] = Field(
        default=None,
        description="URL to download or view the ticket (PDF)"
    )


# PUBLIC_INTERFACE
class PaymentRequest(BaseModel):
    """Initiate payment request for a booking."""

    booking_id: int = Field(..., description="Booking ID")
    payment_method: str = Field(..., description="Payment method")


# PUBLIC_INTERFACE
class TicketResponse(BaseModel):
    """Ticket download/summary response."""

    booking_id: int = Field(..., description="Booking unique ID")
    ticket_url: str = Field(..., description="URL to download/view the ticket")
    seat_numbers: List[str] = Field(..., description="Booked seat numbers")


# PUBLIC_INTERFACE
class BookingHistoryResponse(BaseModel):
    """Booking history for a user."""

    booking_id: int = Field(..., description="Booking unique ID")
    bus_info: BusInfo = Field(..., description="Bus details")
    seat_numbers: List[str] = Field(..., description="Booked seat numbers")
    booking_date: datetime = Field(..., description="Actual time of booking")
    travel_date: date = Field(..., description="Date of travel")
    status: str = Field(..., description="Status of the booking")
    payment_status: str = Field(..., description="Status of the payment")
