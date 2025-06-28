import React from 'react';
import { useParams } from 'react-router-dom';

function SeatSelectionPage() {
  const { busId } = useParams();
  // TODO: Fetch and display seat map for busId, handle seat selection
  return (
    <div>
      <h2>Select Seats for Bus {busId}</h2>
      <p>Seat map and selection UI coming soon</p>
    </div>
  )
}

export default SeatSelectionPage;
