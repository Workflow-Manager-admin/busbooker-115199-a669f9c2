from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import router, openapi_tags

app = FastAPI(
    title="Bus Ticket Booking API",
    description=(
        "FastAPI backend providing API endpoints for bus search, seat selection, "
        "booking, ticket management, and payment processing."
    ),
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


# PUBLIC_INTERFACE
@app.get("/", summary="API Health Check", tags=["Utility"])
def health_check():
    """Returns API liveness status.

    Returns:
        dict: {"message": "Healthy"}
    """
    return {"message": "Healthy"}
