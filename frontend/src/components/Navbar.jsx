import { Link } from "react-router-dom";
import Logo from "./brand/Logo";

export default function Navbar({ user, onLogout }) {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand-link">
          <Logo layout="horizontal" wordmarkSize="sm" />
        </Link>
        <nav className="navbar-nav">
          {user ? (
            <>
              <span className="navbar-user">{user.username}</span>
              <button
                type="button"
                className="btn btn-sm btn-ghost"
                onClick={onLogout}
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-sm btn-ghost">
                Log in
              </Link>
              <Link to="/register" className="btn btn-sm btn-primary">
                Sign up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
