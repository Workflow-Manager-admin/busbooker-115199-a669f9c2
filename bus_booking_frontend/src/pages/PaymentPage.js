import React from 'react';
import { useParams } from 'react-router-dom';

function PaymentPage() {
  const { bookingId } = useParams();
  // TODO: Implement payment form and submission for bookingId
  return (
    <div>
      <h2>Payment</h2>
      <p>Pay for Booking ID: {bookingId}</p>
    </div>
  )
}

export default PaymentPage;
