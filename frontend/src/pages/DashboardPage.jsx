// ✅ src/pages/DashboardPage.jsx
import { useEffect, useState } from "react";
import {
  Chart,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Doughnut, Bar } from "react-chartjs-2";
import { motion } from "framer-motion";
import API from "../api";
import "./dashboard.css"; // ✅ déplacer le fichier ici

Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    API.get("core/dashboard/stats/")
      .then((res) => {
        setStats(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur API :", err);
        setLoading(false);
      });
  }, []);

  if (loading)
    return (
      <div className="loader-container">
        <div className="spinner"></div>
        <p>Chargement du tableau de bord...</p>
      </div>
    );

  if (!stats) return <p className="error">Aucune donnée disponible.</p>;

  const barData = {
    labels: ["Étudiants", "Professeurs", "Programmes", "Articles", "Messages"],
    datasets: [
      {
        label: "Effectifs et contenus",
        data: [
          stats.students_count,
          stats.professors_count,
          stats.programs_count,
          stats.articles_count,
          stats.messages_count,
        ],
        backgroundColor: ["#FFD700", "#00b4d8", "#010120", "#e63946", "#009688"],
      },
    ],
  };

  const activityData = {
    labels: ["Likes", "Unlikes", "Commentaires", "Abonnés"],
    datasets: [
      {
        data: [
          stats.likes_count,
          stats.unlikes_count,
          stats.comments_count,
          stats.abonnes_count,
        ],
        backgroundColor: ["#FFD700", "#e63946", "#010120", "#00b4d8"],
        borderColor: "#ffffff",
        borderWidth: 2,
      },
    ],
  };

  return (
    <motion.div
      className="dashboard-wrapper"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
    >
      <header className="dashboard-header">
        <h1>🏫 Collège Quisqueya — Tableau de bord</h1>
        <p>
          Année académique active : <strong>{stats.active_year}</strong>
        </p>
      </header>

      <section className="stats-section">
        {[
          { label: "Étudiants", value: stats.students_count, icon: "👩‍🎓" },
          { label: "Professeurs", value: stats.professors_count, icon: "👨‍🏫" },
          { label: "Articles", value: stats.articles_count, icon: "📰" },
          { label: "Messages", value: stats.messages_count, icon: "💬" },
          { label: "Dons", value: stats.donations_count, icon: "💰" },
          { label: "Utilisateurs", value: stats.total_users, icon: "👥" },
        ].map((item, index) => (
          <motion.div
            key={index}
            className="stat-card"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="icon">{item.icon}</div>
            <h3>{item.label}</h3>
            <p>{item.value}</p>
          </motion.div>
        ))}
      </section>

      <section className="charts-section">
        <div className="chart-card">
          <h4>Répartition globale</h4>
          <Bar data={barData} />
        </div>

        <div className="chart-card">
          <h4>Interactions</h4>
          <Doughnut data={activityData} />
        </div>
      </section>

      <div className="admin-access">
        <a
          href="http://localhost:8000/admin/"
          target="_blank"
          rel="noopener noreferrer"
          className="admin-btn"
        >
          🛠️ Ouvrir le panneau d'administration Django
        </a>
      </div>
    </motion.div>
  );
}
