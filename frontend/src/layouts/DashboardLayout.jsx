// ✅ src/layouts/DashboardLayout.jsx
import { Outlet, NavLink, useLocation } from "react-router-dom";
import { useEffect } from "react";
import "./dashboard-layout.css";

// ✅ Export nommé, compatible avec { DashboardLayout } dans App.jsx
export function DashboardLayout() {
  const location = useLocation();

  useEffect(() => {
    document.title = "Tableau de bord - Collège Quisqueya";
  }, [location.pathname]);

  return (
    <div className="dashboard-layout">
      {/* 🧭 Barre latérale */}
      <aside className="sidebar">
        <h2 className="sidebar-title">📊 Tableau de bord</h2>

        <nav className="sidebar-nav">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive ? "active-link" : undefined
            }
          >
            🏠 Accueil
          </NavLink>

          <NavLink
            to="/dashboard/students"
            className={({ isActive }) =>
              isActive ? "active-link" : undefined
            }
          >
            👩‍🎓 Étudiants
          </NavLink>

          <NavLink
            to="/dashboard/professors"
            className={({ isActive }) =>
              isActive ? "active-link" : undefined
            }
          >
            👨‍🏫 Professeurs
          </NavLink>

          <a
            href="http://localhost:8000/admin/"
            target="_blank"
            rel="noopener noreferrer"
          >
            ⚙️ Admin Django
          </a>
        </nav>
      </aside>

      {/* 🧱 Contenu principal */}
      <main className="dashboard-content">
        <Outlet />
      </main>
    </div>
  );
}
