import { useState, useEffect } from "react";
import "../pages/dashboard.css";

export function DashboardHeader({ onToggleSidebar, sidebarOpen }) {
  const [theme, setTheme] = useState(
    document.body.classList.contains("dark") ? "dark" : "light"
  );
  const [isSticky, setIsSticky] = useState(false);

  const toggleTheme = () => {
    if (theme === "dark") {
      document.body.classList.remove("dark");
      setTheme("light");
    } else {
      document.body.classList.add("dark");
      setTheme("dark");
    }
  };

  useEffect(() => {
    const handleScroll = () => setIsSticky(window.scrollY > 10);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header className={`dashboard-header ${isSticky ? "sticky-shadow" : ""}`}>
      {/* ✅ Bouton animé ☰ → ✖️ */}
      <button
        className={`menu-toggle ${sidebarOpen ? "open" : ""}`}
        onClick={onToggleSidebar}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <h2>📈 Espace Administration</h2>

      <div className="dashboard-header-actions">
        <div className="theme-container">
          <button className="theme-toggle" onClick={toggleTheme}>
            {theme === "dark" ? "🌞" : "🌙"}
          </button>
        </div>

        <div className="dashboard-user">
          <img
            src="https://cdn-icons-png.flaticon.com/512/3177/3177440.png"
            alt="Profil"
            className="dashboard-user-img"
          />
          <span>Admin</span>
        </div>
      </div>
    </header>
  );
}
