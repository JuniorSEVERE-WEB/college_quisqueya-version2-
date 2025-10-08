import "../pages/dashboard.css";


export function DashboardHeader() {
  return (
    <header className="dashboard-header">
      <h2>📈 Espace Administration</h2>
      <div className="dashboard-user">
        <img
          src="https://cdn-icons-png.flaticon.com/512/3177/3177440.png"
          alt="Profil"
          className="dashboard-user-img"
        />
        <span>Admin</span>
      </div>
    </header>
  );
}
