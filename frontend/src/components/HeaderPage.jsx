import './headerpage.css'
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
export function HeaderPage()
{
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const handleMenuClick = () => setIsMenuOpen(!isMenuOpen);
    const handleLinkClick = () => setIsMenuOpen(false);

    const navigate = useNavigate();
    // Vérifie si l'utilisateur est connecté
    const isLoggedIn = !!localStorage.getItem('access_token');

    const handleLogoutClick = (e) => {
        e.preventDefault();
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsMenuOpen(false);
        navigate('/');
    };

    return(
        <>
           {isMenuOpen && <div className="menu-overlay" onClick={handleMenuClick}></div>}
          <div className="header">
            <div className="left-section">
                <a href="#">
                    <ul>
                        <li><img src="/logo-19-aout.png" alt="Logo" /></li>
                        <li><span>CCM</span></li>
                    </ul>
                </a>
            </div>
            <div className={`middle-section${isMenuOpen ? " show-menu" : ""}`}>
                {/* menu-header-row supprimé : logo et close-menu */}
                <div className="menu-header-row">
                    <div className="menu-logo">
                        <img src="/logo-19-aout.png" alt="Logo" />
                    </div>
                    <button className="close-menu" onClick={handleMenuClick} style={{display: isMenuOpen ? 'block' : 'none'}}>✕</button>
                </div>
                <ul>
                    <li><a href="/" onClick={handleLinkClick}>Accueil</a></li>
                    <li><a href="/about-us" onClick={handleLinkClick}>A propos</a></li>
                    <li><a href="/news" onClick={handleLinkClick}>Actualité</a></li>
                    
                        {!isLoggedIn && <li><a href="/login" onClick={handleLinkClick}>Connexion</a></li>}
                        {!isLoggedIn && <li><a href="/register" onClick={handleLinkClick}>Vie scolaire</a></li>}
                        
                
                </ul>
                <button className="deconnexion mobile-only"><a href="/contact" onClick={handleLinkClick}>Contact</a></button>
            </div>
            <div className="right-section">
                <ul>
                    <button><a href="/contact">Contact</a></button>
                    <li className="menu-icon" onClick={handleMenuClick}>
                         {isMenuOpen? '✕' : '☰'}
                    </li>
                </ul>
            </div>
          </div>
        </>
    );
}