// ✅ frontend/src/App.jsx
import "./App.css";
import { useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import API from "./api";

// 🌐 Pages principales
import NewsPage from "./pages/NewsPage";
import { AboutPage } from "./pages/AboutPage";
import { SchoolLife } from "./pages/SchoolLife";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";
import { ContactPage } from "./pages/ContactPage";
import { HomePage } from "./pages/HomePage";
import { DonationPage } from "./pages/DonationPage";
import ArticleDetailPage from "./pages/ArticleDetailPage";

// 🧭 Dashboard et sous-pages
import { DashboardLayout } from "./layouts/DashboardLayout";
import { DashboardPage } from "./pages/DashboardPage";
import { StudentsManager } from "./pages/StudentsManager";
import { ProfessorsManager } from "./pages/ProfessorsManager";

// 💌 Mot de passe oublié / réinitialisation
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";


// 🔁 Hook : rafraîchit automatiquement le token toutes les 10 min
function useAutoRefreshToken() {
  useEffect(() => {
    const interval = setInterval(async () => {
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) {
        try {
          const { data } = await API.post("auth/token/refresh/", { refresh });
          localStorage.setItem("access_token", data.access);
          window.dispatchEvent(new Event("authChanged"));
          console.log("✅ Access token refreshed automatically");
        } catch (err) {
          console.warn("⚠️ Token refresh failed:", err);
        }
      }
    }, 1000 * 60 * 10); // ⏱️ toutes les 10 minutes

    return () => clearInterval(interval);
  }, []);
}


function App() {
  useAutoRefreshToken();

  return (
    <Routes>
      {/* 🌐 Pages publiques */}
      <Route path="/" element={<HomePage />} />
      <Route path="/about" element={<AboutPage />} />
      <Route path="/schoollife" element={<SchoolLife />} />
      <Route path="/contact" element={<ContactPage />} />
      <Route path="/donation" element={<DonationPage />} />
      <Route path="/news" element={<NewsPage />} />
      <Route path="/news/:id" element={<ArticleDetailPage />} />

      {/* 🔐 Authentification */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/profile" element={<ProfilePage />} />

      {/* 🧭 Tableau de bord */}
      <Route path="/dashboard" element={<DashboardLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="students" element={<StudentsManager />} />
        <Route path="professors" element={<ProfessorsManager />} />
      </Route>

      {/* 💌 Mot de passe oublié / reset */}
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset/:uidb64/:token/" element={<ResetPassword />} />
    </Routes>
  );
}

export default App;
