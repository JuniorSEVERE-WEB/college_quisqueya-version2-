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
import API from "../api"; // axios configuré
import "./dashboard.css";

Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  // 1️⃣ Charger les statistiques du backend
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    console.log("🎫 Access token trouvé :", token ? "✅ Oui" : "❌ Non");

    API.get("core/dashboard/stats/")
      .then((res) => {
        console.log("✅ Réponse API :", res.data);
        setStats(res.data);
      })
      .catch((err) => {
        console.error("❌ Erreur API :", err.response || err);
        setError("Impossible de charger les statistiques.");
      });
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!stats) return <p className="loading">Chargement des statistiques...</p>;

  // 2️⃣ Graphique Doughnut : Répartition garçons / filles
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

  // 3️⃣ Graphique Bar : Statistiques globales
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

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">📊 Tableau de bord de l’école</h1>
      <p className="academic-year">
        Année académique active : <strong>{stats.academic_year}</strong>
      </p>

      {/* 4️⃣ Cartes KPI principales */}
      <div className="kpi-grid">
        <KpiCard title="👩‍🎓 Étudiants" value={stats.students_total} />
        <KpiCard title="👨‍🏫 Professeurs" value={stats.professors_total} />
        <KpiCard title="💼 Employés" value={stats.employees_total} />
        <KpiCard title="💰 Paiements" value={`${stats.payments_total} Gdes`} />
        <KpiCard title="🎁 Dons" value={`${stats.donations_total} Gdes`} />
        <KpiCard title="🎓 Alumni" value={stats.alumni_total} />
        <KpiCard title="📰 Abonnés" value={stats.subscribers_total} />
      </div>

      {/* 5️⃣ Graphiques */}
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
    </div>
  );
}

// ✅ Composant pour afficher les KPI Cards
function KpiCard({ title, value }) {
  return (
    <div className="kpi-card">
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}
