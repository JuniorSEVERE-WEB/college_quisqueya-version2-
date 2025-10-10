// frontend/src/components/HeaderPage.jsx
import "./headerpage.css";
import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";

export function HeaderPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );
  const [role, setRole] = useState(localStorage.getItem("role") || "");

  const handleMenuClick = () => setIsMenuOpen(!isMenuOpen);
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
        {/* Section gauche : logo */}
        <div className="left-section">
          <Link to="/" onClick={handleLinkClick}>
            <ul>
              <li>
                <img src="/logo-19-aout.png" alt="Logo" />
              </li>
              <li>
                <span>CQL</span>
              </li>
            </ul>
          </Link>
        </div>

        {/* Section menu principale (mobile) */}
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
                A propos
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

            {/* ✅ Dashboard visible uniquement pour l’admin connecté */}
            {isLoggedIn && role === "admin" && (
              <li>
                <Link to="/dashboard" onClick={handleLinkClick}>
                  🏫 Dashboard
                </Link>
              </li>
            )}

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
            <li>
              <Link to="/contact" onClick={handleLinkClick}>
                Contact
              </Link>
            </li>
          </ul>
        </div>

        {/* Section droite (desktop) */}
        <div className="right-section">
          <ul>
            {/* ✅ Dashboard visible sur desktop aussi */}
            {isLoggedIn && role === "admin" && (
              <li>
                <Link to="/dashboard" className="contact-btn">
                  🏫 Dashboard
                </Link>
              </li>
            )}
            <li>
              <Link to="/contact" className="contact-btn">
                Contact
              </Link>
            </li>
            <li className="menu-icon" onClick={handleMenuClick}>
              {isMenuOpen ? "✕" : "☰"}
            </li>
          </ul>
        </div>
      </div>
    </>
  );
}
