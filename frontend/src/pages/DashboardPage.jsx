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
import API from "../api";
import "./dashboard.css";

Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    // Charger les statistiques
    API.get("core/dashboard/stats/")
      .then((res) => setStats(res.data))
      .catch(() => setError("Erreur de chargement des statistiques"));

    // Charger les graphiques
    API.get("core/dashboard/chart-data/")
      .then((res) => setChartData(res.data))
      .catch(() => setError("Erreur de chargement des graphiques"));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!stats || !chartData) return <p>Chargement des données...</p>;

  // ✅ Protection contre undefined
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

  return (
    <div className="dashboard-container">
      <h1>Tableau de bord</h1>

      <div className="stats-grid">
        <div className="card">
          <h3>Étudiants</h3>
          <p>{stats.students_count}</p>
        </div>
        <div className="card">
          <h3>Professeurs</h3>
          <p>{stats.professors_count}</p>
        </div>
        <div className="card">
            <h3>Abonnés</h3>
            <p>{stats.abonnes_count}</p>
       </div>
        <div className="card">
          <h3>Total utilisateurs</h3>
          <p>{stats.total_users}</p>
        </div>
        <div className="card">
          <h3>Messages non lus</h3>
          <p>{stats.unread_messages}</p>
        </div>
      </div>

      <div className="charts">
        <div className="chart-card">
          <h3>Répartition par sexe (étudiants)</h3>
          <Doughnut data={genderData} />
        </div>


        <div className="chart-card">
          <h3>Inscriptions par mois</h3>
          <Bar data={monthlyData} />
        </div>

        <div className="chart-card">
          <h3>Répartition par programme</h3>
          <Bar data={programData} />
        </div>
      </div>

      <div className="chart-card">
            <h3>Abonnés par mois</h3>
            <Bar
                data={{
                labels: chartData.abonnes_per_month?.labels || [],
                datasets: [
                    {
                    label: "Nouveaux abonnés",
                    data: chartData.abonnes_per_month?.data || [],
                    backgroundColor: "#4CAF50",
                    },
                ],
                }}
            />
        </div>

      <div className="footer">
        <p>
          Année académique active : <strong>{stats.active_year}</strong>
        </p>
      </div>
    </div>
  );
}

export default DashboardPage;
