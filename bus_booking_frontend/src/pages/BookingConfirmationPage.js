import React from 'react';
import { useParams } from 'react-router-dom';

function BookingConfirmationPage() {
  const { bookingId } = useParams();
  // TODO: Fetch and show booking confirmation details
  return (
    <div>
      <h2>Booking Confirmation</h2>
      <p>Booking ID: {bookingId}</p>
    </div>
  )
}

export default BookingConfirmationPage;
