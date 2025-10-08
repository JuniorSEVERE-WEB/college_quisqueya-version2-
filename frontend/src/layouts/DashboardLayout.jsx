import { Outlet } from "react-router-dom";
import { DashboardSidebar } from "../components/DashboardSidebar";
import { DashboardHeader } from "../components/DashboardHeader";
import "../pages/dashboard.css";

export function DashboardLayout() {
  return (
    <div className="dashboard-layout">
      <DashboardSidebar />
      <main className="dashboard-main">
        <DashboardHeader />
        <div className="dashboard-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
