import { Link, useLocation } from "react-router-dom";
import "../pages/dashboard.css";


export function DashboardSidebar() {
  const location = useLocation();

  const menuItems = [
    { path: "/dashboard", label: "Tableau de bord" },
    { path: "/dashboard/students", label: "Étudiants" },
    { path: "/dashboard/professors", label: "Professeurs" },
  ];

  return (
    <aside className="dashboard-sidebar">
      <div className="dashboard-logo">
        🎓 Collège Quisqueya
      </div>
      <nav>
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`dashboard-link ${
              location.pathname === item.path ? "active" : ""
            }`}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
