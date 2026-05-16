// frontend/src/components/HeaderPage.jsx
import "./headerpage.css";
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../api";

const DEFAULT_LOGO = "/logo-19-aout.png";

export function HeaderPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );
  const [role, setRole] = useState(localStorage.getItem("role") || "");
  const [logoUrl, setLogoUrl] = useState(DEFAULT_LOGO);
  const [siteName, setSiteName] = useState("CQL");

  useEffect(() => {
    API.get("homepage/settings/")
      .then((res) => {
        if (res.data?.logo) setLogoUrl(res.data.logo);
        if (res.data?.site_name) setSiteName(res.data.site_name);
      })
      .catch(() => {});
  }, []);

  const handleMenuClick = () => {
    const menu = document.querySelector(".middle-section");
    if (isMenuOpen && menu) {
      menu.classList.add("closing");
      setTimeout(() => {
        menu.classList.remove("closing");
        setIsMenuOpen(false);
      }, 300);
    } else {
      setIsMenuOpen(true);
    }
  };

  const handleLinkClick = () => setIsMenuOpen(false);

  useEffect(() => {
    const update = () => {
      setIsLoggedIn(!!localStorage.getItem("access_token"));
      setRole(localStorage.getItem("role") || "");
    };
    update();
    window.addEventListener("storage", update);
    window.addEventListener("authChanged", update);
    return () => {
      window.removeEventListener("storage", update);
      window.removeEventListener("authChanged", update);
    };
  }, []);

  const navigate = useNavigate();

  const handleLogoutClick = (e) => {
    e.preventDefault();
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    localStorage.removeItem("role");
    setIsMenuOpen(false);
    window.dispatchEvent(new Event("authChanged"));
    navigate("/");
  };

  return (
    <>
      {isMenuOpen && (
        <div className="menu-overlay" onClick={handleMenuClick}></div>
      )}
      <div className="header">
        {/* --- SECTION GAUCHE --- */}
        <div className="left-section">
          <Link to="/" onClick={handleLinkClick}>
            <ul>
              <li>
                <img
                  src={logoUrl}
                  alt="Logo"
                  onError={(e) => {
                    e.currentTarget.src = DEFAULT_LOGO;
                  }}
                />
              </li>
              <li>
                <span>{siteName}</span>
              </li>
            </ul>
          </Link>
        </div>

        {/* --- MENU CENTRAL (LIENS PRINCIPAUX) --- */}
        <div className={`middle-section${isMenuOpen ? " show-menu" : ""}`}>
          <div className="menu-header-row">
            <button
              className="close-menu"
              onClick={handleMenuClick}
              style={{
                display: isMenuOpen ? "block" : "none",
                margin: "0 auto",
              }}
            >
              ✕
            </button>
          </div>

          <ul>
            <li>
              <Link to="/" onClick={handleLinkClick}>
                Accueil
              </Link>
            </li>
            <li>
              <Link to="/about" onClick={handleLinkClick}>
                À propos
              </Link>
            </li>
            <li>
              <Link to="/news" onClick={handleLinkClick}>
                Actualité
              </Link>
            </li>
            <li>
              <Link to="/schoollife" onClick={handleLinkClick}>
                Vie Scolaire
              </Link>
            </li>

            {/* 🔹 Connexion / Déconnexion */}
            {!isLoggedIn && (
              <li>
                <Link to="/login" onClick={handleLinkClick}>
                  Connexion
                </Link>
              </li>
            )}
            {isLoggedIn && (
              <li>
                <a href="#" onClick={handleLogoutClick}>
                  Déconnexion
                </a>
              </li>
            )}

            {/* ✅ --- BOUTONS MOBILE (Contact + Dashboard) --- */}
            <div className="mobile-menu-buttons">
              {/* Dashboard admin uniquement */}
              {isLoggedIn && role === "admin" && (
                <Link
                  to="/dashboard"
                  className="mobile-btn mobile-dashboard"
                  onClick={handleLinkClick}
                >
                  🏫 Dashboard
                </Link>
              )}

              {/* Bouton Contact toujours visible sur mobile */}
              <Link
                to="/contact"
                className="mobile-btn mobile-contact"
                onClick={handleLinkClick}
              >
                ✉️ Contact
              </Link>
            </div>
          </ul>
        </div>

        {/* --- SECTION DROITE (DESKTOP) --- */}
        <div className="right-section">
          <ul>
            {/* ✅ Dashboard visible sur desktop uniquement pour l’admin */}
            {isLoggedIn && role === "admin" && (
              <li>
                <Link to="/dashboard" className="contact-btn">
                  🏫 Dashboard
                </Link>
              </li>
            )}

            {/* ✅ Contact visible sur desktop */}
            <li>
              <Link to="/contact" className="contact-btn">
                ✉️ Contact
              </Link>
            </li>

            {/* Bouton menu mobile */}
            <li className="menu-icon" onClick={handleMenuClick}>
              {isMenuOpen ? "✕" : "☰"}
            </li>
          </ul>
        </div>
      </div>
    </>
  );
}
