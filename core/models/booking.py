from datetime import date
from typing import Optional
from pydantic import BaseModel

class BookingDates(BaseModel):
    checkin: date
    checkout: date

class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None

class BookingResponse(BaseModel):
    bookingid: int
    booking: Booking
