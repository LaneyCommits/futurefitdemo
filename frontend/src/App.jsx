import { BrowserRouter, Navigate, Route, Routes, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing";
import Quiz from "./pages/Quiz";
import Results from "./pages/Results";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import useAuth from "./hooks/useAuth";

function AppRoutes({ user, saveToken, logout }) {
  const location = useLocation();
  const immersiveRoutes = ["/", "/quiz"];
  const hideNav = immersiveRoutes.includes(location.pathname);

  return (
    <div className="page-shell">
      {!hideNav && <Navbar user={user} onLogout={logout} />}
      <main className="page-main">
        <Routes>
          <Route path="/" element={<Landing user={user} />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/results" element={<Results user={user} />} />
          <Route path="/login" element={<Login onAuth={saveToken} user={user} />} />
          <Route
            path="/register"
            element={<Register onAuth={saveToken} user={user} />}
          />
          <Route
            path="/dashboard"
            element={user ? <Dashboard /> : <Navigate to="/login" replace />}
          />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  const { user, loading, saveToken, logout } = useAuth();

  if (loading) {
    return (
      <div className="page-center">
        <div className="loading-spinner" />
      </div>
    );
  }

  return (
    <BrowserRouter>
      <AppRoutes user={user} saveToken={saveToken} logout={logout} />
    </BrowserRouter>
  );
}
