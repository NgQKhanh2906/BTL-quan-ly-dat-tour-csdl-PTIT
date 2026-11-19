import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { MotionConfig } from 'framer-motion';
import { AuthProvider } from './context/AuthContext';
import { UserLayout } from './components/layout/UserLayout';
import LandingPage from './pages/user/LandingPage';
import ExplorePage from './pages/user/ExplorePage';
import BookingPage from './pages/user/BookingPage';
import ReviewsPage from './pages/user/ReviewsPage';
import { AdminOrdersPage } from './pages/admin/AdminOrdersPage';
import { AdminConfirmationsPage } from './pages/admin/AdminConfirmationsPage';
import { AdminDashboardPage } from './pages/admin/AdminDashboardPage';

export default function App() {
  return (
    <MotionConfig reducedMotion="user">
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<UserLayout />}>
              <Route path="/" element={<LandingPage />} />
              <Route path="/explore" element={<ExplorePage />} />
              <Route path="/book" element={<BookingPage />} />
              <Route path="/orders" element={<AdminOrdersPage />} />
              <Route path="/reviews" element={<ReviewsPage />} />
              <Route path="/confirmations" element={<AdminConfirmationsPage />} />
              <Route path="/reports" element={<AdminDashboardPage />} />

              {/* Chuyển hướng các đường dẫn cũ sang form tương ứng */}
              <Route path="/my-bookings" element={<Navigate to="/orders" replace />} />
              <Route path="/admin" element={<Navigate to="/orders" replace />} />
              <Route path="/admin/login" element={<Navigate to="/orders" replace />} />
              <Route path="/admin/orders" element={<Navigate to="/orders" replace />} />
              <Route path="/admin/dashboard" element={<Navigate to="/reports" replace />} />
              <Route path="/admin/confirmations" element={<Navigate to="/confirmations" replace />} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </MotionConfig>
  );
}
