import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Doughnut, Bar } from "react-chartjs-2";
import {
  Chart,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import API from "../api";
import "./dashboard.css";

Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    API.get("core/dashboard/stats/")
      .then((res) => setStats(res.data))
      .catch(() => setError("Impossible de charger les statistiques."));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!stats) return <p className="loading">Chargement des statistiques...</p>;

  const sexData = {
    labels: ["Garçons", "Filles"],
    datasets: [
      {
        data: [stats.students_male, stats.students_female],
        backgroundColor: ["#1E3A8A", "#F472B6"],
        borderWidth: 1,
      },
    ],
  };

  const totalsData = {
    labels: [
      "Élèves",
      "Professeurs",
      "Employés",
      "Alumni",
      "Abonnés",
      "Articles",
      "Commentaires",
    ],
    datasets: [
      {
        label: "Totaux",
        data: [
          stats.students_total,
          stats.professors_total,
          stats.employees_total,
          stats.alumni_total,
          stats.subscribers_total,
          stats.articles_total,
          stats.comments_total,
        ],
        backgroundColor: [
          "#3B82F6",
          "#22C55E",
          "#F59E0B",
          "#8B5CF6",
          "#0EA5E9",
          "#F43F5E",
          "#14B8A6",
        ],
      },
    ],
  };

  const links = [
    { path: "/dashboard", label: "📊 Dashboard" },
    { path: "/dashboard/students", label: "👩‍🎓 Students" },
    { path: "/dashboard/professors", label: "👨‍🏫 Professors" },
    { path: "/dashboard/employees", label: "💼 Employees" },
    { path: "/dashboard/payments", label: "💰 Payments" },
    { path: "/dashboard/blog", label: "📰 Blog" },
  ];

  return (
    <div className="dashboard-layout">
      {/* ===== HEADER MOBILE ===== */}
      <header className="dashboard-header">
        <button
          className="menu-toggle"
          onClick={() => setSidebarOpen((prev) => !prev)}
        >
          ☰
        </button>
        <h1>Tableau de bord</h1>
      </header>

      {/* ===== SIDEBAR ===== */}
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <h2 className="sidebar-title">Collège Quisqueya</h2>
        <nav>
          {links.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={location.pathname === link.path ? "active" : ""}
              onClick={() => setSidebarOpen(false)} // referme après clic mobile
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <button
          className="logout-btn"
          onClick={() => {
            localStorage.clear();
            window.location.href = "/";
          }}
        >
          🚪 Logout
        </button>
      </aside>

      {/* ===== MAIN ===== */}
      <main className="dashboard-main" onClick={() => sidebarOpen && setSidebarOpen(false)}>
        <p className="academic-year">
          Année académique : <strong>{stats.academic_year}</strong>
        </p>

        <div className="kpi-grid">
          <KpiCard title="👩‍🎓 Étudiants" value={stats.students_total} />
          <KpiCard title="👨‍🏫 Professeurs" value={stats.professors_total} />
          <KpiCard title="💼 Employés" value={stats.employees_total} />
          <KpiCard title="💰 Paiements" value={`${stats.payments_total} Gdes`} />
          <KpiCard title="🎁 Dons" value={`${stats.donations_total} Gdes`} />
          <KpiCard title="🎓 Alumni" value={stats.alumni_total} />
          <KpiCard title="📰 Abonnés" value={stats.subscribers_total} />
        </div>

        <div className="charts-container">
          <div className="chart-box">
            <h2>Répartition Filles / Garçons</h2>
            <Doughnut data={sexData} />
          </div>

          <div className="chart-box">
            <h2>Statistiques globales</h2>
            <Bar data={totalsData} />
          </div>
        </div>
      </main>
    </div>
  );
}

function KpiCard({ title, value }) {
  return (
    <div className="kpi-card">
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}
