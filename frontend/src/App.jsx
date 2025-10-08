import NewsPage from "./pages/NewsPage";
import "./App.css";

import { AboutPage } from "./pages/AboutPage";
import { SchoolLife } from "./pages/SchoolLife";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";
import { ContactPage } from "./pages/ContactPage";
import { HomePage } from "./pages/HomePage";
import { DonationPage } from "./pages/DonationPage";
import ArticleDetailPage from "./pages/ArticleDetailPage";
import { DashboardPage } from "./pages/DashboardPage";
import { StudentsManager } from "./pages/StudentsManager";
import { ProfessorsManager } from "./pages/ProfessorsManager";

import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { useEffect } from "react";
import { DashboardLayout } from "./layouts/DashboardLayout";

// ✅ Chargement conditionnel du CSS du dashboard
function ConditionalDashboardCSS() {
  const location = useLocation();

  useEffect(() => {
    if (location.pathname.startsWith("/dashboard")) {
      import("./pages/dashboard.css");
    }
  }, [location.pathname]);

  return null;
}

function App() {
  return (
    <Router>
      <ConditionalDashboardCSS />

      <Routes>
        {/* 🌐 Pages principales */}
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/schoollife" element={<SchoolLife />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/donation" element={<DonationPage />} />
        <Route path="/news" element={<NewsPage />} />
        <Route path="/news/:id" element={<ArticleDetailPage />} />

        {/* 🔐 Auth */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/profile" element={<ProfilePage />} />

        {/* 🧭 Dashboard (avec Layout dédié) */}
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/dashboard/students" element={<StudentsManager />} />
          <Route path="/dashboard/professors" element={<ProfessorsManager />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
