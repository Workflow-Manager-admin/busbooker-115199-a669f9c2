from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List
from datetime import date

from . import models, services


# Tag definitions for OpenAPI grouping
openapi_tags = [
    {"name": "Auth", "description": "User registration, login, authentication"},
    {"name": "Bus", "description": "Bus search and listing"},
    {"name": "Seat", "description": "Seat selection and seat map"},
    {"name": "Booking", "description": "Ticket booking and booking management"},
    {"name": "Payment", "description": "Payment processing"},
    {"name": "Ticket", "description": "Ticket download"},
]

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def _fake_decode_token(token: str) -> int:
    """
    Returns a user_id extracted from fake token.
    In production, decode JWT here.
    """
    try:
        parts = token.split("-")
        return int(parts[1])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    return _fake_decode_token(token)


# --- Auth Endpoints ---


@router.post(
    "/auth/register",
    tags=["Auth"],
    summary="Register a new user",
    description="Registers a new user with username, email, and password.",
    response_model=models.UserResponse,
    status_code=201,
)
def register_user(payload: models.UserRegisterRequest):
    try:
        return services.register_user(payload)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.post(
    "/auth/login",
    tags=["Auth"],
    summary="User login",
    response_model=models.TokenResponse,
)
def login_user(payload: models.UserLoginRequest):
    user = services.authenticate_user(payload)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = services.generate_jwt_token(user)
    return models.TokenResponse(access_token=token, token_type="bearer")


# --- Bus Search/List Endpoints ---


@router.post(
    "/buses/search",
    tags=["Bus"],
    summary="Search buses by route and date",
    response_model=List[models.BusInfo],
)
def search_buses(payload: models.BusSearchRequest):
    return services.search_buses(payload)


# --- Seat Selection Endpoints ---


@router.get(
    "/seats/{bus_id}",
    tags=["Seat"],
    summary="Get seat map for a bus",
    response_model=List[models.SeatInfo],
)
def seats_map(
    bus_id: int,
    travel_date: date = Query(..., description="Desired travel date"),
):
    return services.get_seat_map(bus_id, travel_date)


# --- Booking and Ticket Endpoints ---


@router.post(
    "/bookings",
    tags=["Booking"],
    summary="Book bus tickets",
    response_model=models.BookingResponse,
)
def book_ticket(
    payload: models.BookingRequest,
    user_id: int = Depends(get_current_user),
):
    try:
        return services.book_tickets(user_id, payload)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.get(
    "/bookings/history",
    tags=["Booking"],
    summary="Get booking history for current user",
    response_model=List[models.BookingHistoryResponse],
)
def booking_history(user_id: int = Depends(get_current_user)):
    return services.get_booking_history(user_id)


@router.get(
    "/tickets/{booking_id}",
    tags=["Ticket"],
    summary="Get ticket details/download link",
    response_model=models.TicketResponse,
)
def get_ticket(
    booking_id: int,
    user_id: int = Depends(get_current_user),
):
    try:
        return services.get_ticket(user_id, booking_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))


# --- Payment Processing ---


@router.post(
    "/payments",
    tags=["Payment"],
    summary="Process payment for a booking",
    response_model=models.BookingResponse,
)
def process_payment(
    payload: models.PaymentRequest,
    user_id: int = Depends(get_current_user),
):
    try:
        return services.process_payment(user_id, payload)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
