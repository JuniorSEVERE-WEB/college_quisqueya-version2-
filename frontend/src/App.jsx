import NewsPage from './pages/NewsPage'


import './App.css'


import { AboutPage } from './pages/AboutPage'
import {SchoolLife} from './pages/SchoolLife'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProfilePage from './pages/ProfilePage'
import {ContactPage} from './pages/ContactPage'
import { HomePage } from './pages/HomePage'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
  <Route path="/" element={<HomePage />} />
  {/* <Route path="/accueil" element={<AccueilPage />} /> */}
  <Route path="/about" element={<AboutPage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route path="/register" element={<RegisterPage />} />
  <Route path="/profile" element={<ProfilePage />} />
  <Route path="/contact" element={<ContactPage />} />
  <Route path="/news" element={<NewsPage />} />
  <Route path="/schoollife" element={<SchoolLife />} />
      </Routes>
    </Router>
  );
}

export default App
