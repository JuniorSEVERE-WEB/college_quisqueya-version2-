import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import "../pages/dashboard.css";

export function DashboardSidebar({ onToggle }) {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(true);

  // Fermer par défaut sur mobile
  useEffect(() => {
    if (window.innerWidth < 768) setIsOpen(false);
  }, []);

  const toggleSidebar = () => {
    const newState = !isOpen;
    setIsOpen(newState);
    onToggle && onToggle(newState);
  };

  const menuItems = [
    { path: "/dashboard", label: "Tableau de bord" },
    { path: "/dashboard/students", label: "Étudiants" },
    { path: "/dashboard/professors", label: "Professeurs" },
  ];

  return (
    <>
      <button
        className="hamburger"
        onClick={toggleSidebar}
        aria-label="Menu"
        type="button"
      >
        ☰
      </button>

      <aside className={`dashboard-sidebar ${isOpen ? "open" : "closed"}`}>
        <div className="dashboard-logo">🎓 Collège Quisqueya</div>
        <nav className="dashboard-nav">
          {menuItems.map(item => (
            <Link
              key={item.path}
              to={item.path}
              className={`dashboard-link ${
                location.pathname === item.path ? "active" : ""
              }`}
              onClick={() => {
                if (window.innerWidth < 768) setIsOpen(false);
              }}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="dashboard-sidebar-footer">
          <small>&copy; {new Date().getFullYear()} CQ</small>
        </div>
      </aside>
    </>
  );
}