import NewsPage from './pages/NewsPage';
import './App.css';

import { AboutPage } from './pages/AboutPage';
import { SchoolLife } from './pages/SchoolLife';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import { ContactPage } from './pages/ContactPage';
import { HomePage } from './pages/HomePage';
import { DonationPage } from "./pages/DonationPage";
import ArticleDetailPage from "./pages/ArticleDetailPage";
import { DashboardPage } from "./pages/DashboardPage"; // ✅ Ajout du Dashboard
import { StudentsManager } from "./pages/StudentsManager"
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ProfessorsManager } from "./pages/ProfessorsManager";


function App() {
  return (
    <Router>
      <Routes>
        {/*  Pages principales */}
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/schoollife" element={<SchoolLife />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/donation" element={<DonationPage />} />
        <Route path="/news" element={<NewsPage />} />
        <Route path="/news/:id" element={<ArticleDetailPage />} />

        {/*  Authentification */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/profile" element={<ProfilePage />} />

        {/*  Tableau de bord */}
        <Route path="/dashboard" element={<DashboardPage />} /> {/* ✅ Nouvelle route */}
        <Route path="/dashboard/students" element={<StudentsManager />} />
        <Route path="/dashboard/professors" element={<ProfessorsManager />} />
       
      </Routes>
    </Router>
  );
}

export default App;
