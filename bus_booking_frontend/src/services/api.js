import axios from 'axios';

// Set backend API base URL
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: BASE_URL,
});

// PUBLIC_INTERFACE
export function registerUser(data) {
  return api.post('/auth/register', data);
}

// PUBLIC_INTERFACE
export function loginUser(data) {
  return api.post('/auth/login', data);
}

// PUBLIC_INTERFACE
export function searchBuses(data) {
  return api.post('/buses/search', data);
}

// Add more functions for seats, bookings, payments, tickets, etc.

export default api;
