import React from 'react';
import { useParams } from 'react-router-dom';

function TicketDownloadPage() {
  const { bookingId } = useParams();
  // TODO: Fetch ticket details, provide download link (PDF)
  return (
    <div>
      <h2>Ticket Download</h2>
      <p>Ticket for Booking ID: {bookingId}</p>
    </div>
  )
}

export default TicketDownloadPage;
