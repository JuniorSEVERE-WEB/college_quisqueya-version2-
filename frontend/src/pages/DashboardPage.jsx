// src/pages/DashboardPage.jsx
import { useEffect, useState } from "react";
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
import { DashboardSidebar } from "../components/DashboardSidebar";
import { DashboardHeader } from "../components/DashboardHeader";
import API from "../api";
import "./dashboard.css";

Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // 🔹 Charger les données
  useEffect(() => {
    API.get("core/dashboard/stats/")
      .then((res) => setStats(res.data))
      .catch(() => setError("Erreur de chargement des statistiques"));

    API.get("core/dashboard/chart-data/")
      .then((res) => setChartData(res.data))
      .catch(() => setError("Erreur de chargement des graphiques"));
  }, []);

  // 🌙 Mode sombre auto
  useEffect(() => {
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");
    const updateTheme = () => {
      if (prefersDark.matches) document.body.classList.add("dark");
      else document.body.classList.remove("dark");
    };
    updateTheme();
    prefersDark.addEventListener("change", updateTheme);
    return () => prefersDark.removeEventListener("change", updateTheme);
  }, []);

  // ⚠️ Gestion des erreurs
  if (error) return <p className="error">{error}</p>;

  // 🌀 Écran de chargement
  if (!stats || !chartData) {
    return (
      <div className="dashboard-loading-screen">
        <div>
          <div className="dashboard-spinner"></div>
          <div className="dashboard-loading-text">
            Chargement du tableau de bord...
          </div>
        </div>
      </div>
    );
  }

  // 📊 Données des graphiques
  const genderData = {
    labels: stats.gender_ratio_students?.labels || [],
    datasets: [
      {
        data: stats.gender_ratio_students?.data || [],
        backgroundColor: ["#FF6384", "#36A2EB"],
      },
    ],
  };

  const monthlyData = {
    labels: chartData?.monthly_registrations?.labels || [],
    datasets: [
      {
        label: "Inscriptions",
        data: chartData?.monthly_registrations?.data || [],
        backgroundColor: "#36A2EB",
      },
    ],
  };

  const programData = {
    labels: chartData?.program_distribution?.labels || [],
    datasets: [
      {
        label: "Étudiants par programme",
        data: chartData?.program_distribution?.data || [],
        backgroundColor: "#FF6384",
      },
    ],
  };

  const abonnesData = {
    labels: chartData.abonnes_per_month?.labels || [],
    datasets: [
      {
        label: "Nouveaux abonnés",
        data: chartData.abonnes_per_month?.data || [],
        backgroundColor: "#4CAF50",
      },
    ],
  };

  // ⚙️ Options de Chart.js
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: document.body.classList.contains("dark") ? "#f4f4f4" : "#333",
        },
      },
    },
    animation: {
      duration: 1200,
      easing: "easeOutQuart",
      delay: (context) => context.dataIndex * 100,
    },
    scales: {
      x: {
        ticks: {
          color: document.body.classList.contains("dark") ? "#f4f4f4" : "#333",
        },
      },
      y: {
        ticks: {
          color: document.body.classList.contains("dark") ? "#f4f4f4" : "#333",
        },
      },
    },
  };

  // ============================
  // 💠 Structure principale
  // ============================
  return (
    <div
      className={`dashboard-layout ${
        sidebarOpen ? "sidebar-open" : "sidebar-closed"
      }`}
    >
      {/* 🔹 Barre latérale */}
      <DashboardSidebar onToggle={setSidebarOpen} />

      {/* 🌫️ Overlay flouté sur mobile */}
      <div
        className="dashboard-overlay"
        onClick={() => setSidebarOpen(false)}
      ></div>

      {/* 🔹 Contenu principal */}
      <main className="dashboard-main">
        <DashboardHeader
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          sidebarOpen={sidebarOpen}
        />

        <div className="dashboard-container">
          <h1 className="dashboard-title">📊 Tableau de bord</h1>

          {/* Cartes de statistiques */}
          <div className="dashboard-stats-grid">
            <div className="dashboard-card dashboard-card-blue">
              <h3>Étudiants</h3>
              <p>{stats.students_count}</p>
            </div>
            <div className="dashboard-card dashboard-card-purple">
              <h3>Professeurs</h3>
              <p>{stats.professors_count}</p>
            </div>
            <div className="dashboard-card dashboard-card-green">
              <h3>Abonnés</h3>
              <p>{stats.abonnes_count}</p>
            </div>
            <div className="dashboard-card dashboard-card-gray">
              <h3>Total utilisateurs</h3>
              <p>{stats.total_users}</p>
            </div>
            <div className="dashboard-card dashboard-card-orange">
              <h3>Messages non lus</h3>
              <p>{stats.unread_messages}</p>
            </div>
          </div>

          {/* Graphiques */}
          <div className="dashboard-charts">
            <div className="dashboard-chart-card">
              <h3>Répartition par sexe (Étudiants)</h3>
              <Doughnut data={genderData} options={chartOptions} />
            </div>

            <div className="dashboard-chart-card">
              <h3>Inscriptions par mois</h3>
              <Bar data={monthlyData} options={chartOptions} />
            </div>

            <div className="dashboard-chart-card">
              <h3>Répartition par programme</h3>
              <Bar data={programData} options={chartOptions} />
            </div>

            <div className="dashboard-chart-card">
              <h3>Abonnés par mois</h3>
              <Bar data={abonnesData} options={chartOptions} />
            </div>
          </div>

          {/* Pied de page */}
          <div className="dashboard-footer">
            <p>
              Année académique active : <strong>{stats.active_year}</strong>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default DashboardPage;
