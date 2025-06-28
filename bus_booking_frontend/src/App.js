import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import SearchPage from './pages/SearchPage';
import SeatSelectionPage from './pages/SeatSelectionPage';
import BookingConfirmationPage from './pages/BookingConfirmationPage';
import BookingHistoryPage from './pages/BookingHistoryPage';
import PaymentPage from './pages/PaymentPage';
import TicketDownloadPage from './pages/TicketDownloadPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/search" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/search" element={<SearchPage />} />
      <Route path="/seats/:busId" element={<SeatSelectionPage />} />
      <Route path="/booking/confirmation/:bookingId" element={<BookingConfirmationPage />} />
      <Route path="/booking/history" element={<BookingHistoryPage />} />
      <Route path="/payment/:bookingId" element={<PaymentPage />} />
      <Route path="/ticket/:bookingId" element={<TicketDownloadPage />} />
    </Routes>
  );
}

export default App;
