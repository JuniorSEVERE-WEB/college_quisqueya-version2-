import { Link } from "react-router-dom";
import { FaMapMarkerAlt, FaEnvelope, FaPhone } from "react-icons/fa";
import { motion } from "framer-motion"; // ✅ Import Framer Motion
import "./footerpage.css";

export function FooterPage() {
  // Variantes d'animation réutilisables
  const fadeInUp = {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <footer className="footer">
      <div className="footer-container">
        {/* Colonne Présentation */}
        <motion.div
          className="footer-col"
          variants={fadeInUp}
          initial="hidden"
          whileInView="visible"
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: false, amount: 0.3 }} // 🔹 rejoue si on remonte/redescend
        >
          <h2 className="footer-title">Collège Quisqueya de Léogâne</h2>
          <p className="footer-text">
            Établissement d’excellence, le Collège Quisqueya de Léogâne accompagne
            chaque élève vers la réussite grâce à un encadrement exigeant et bienveillant.
          </p>
        </motion.div>

        {/* Colonne Menu */}
        <motion.div
          className="footer-col"
          variants={fadeInUp}
          initial="hidden"
          whileInView="visible"
          transition={{ duration: 0.8, delay: 1 }}
          viewport={{ once: false, amount: 0.3 }}
        >
          <h2 className="footer-title">Menu</h2>
          <ul className="footer-links">
            <li><Link to="/donation">Donation</Link></li>
            <li><Link to="/">Accueil</Link></li>
            <li><Link to="/about">À propos</Link></li>
            <li><Link to="/contact">Contact</Link></li>
            <li><Link to="/login">Connexion</Link></li>
            <li><Link to="/logout">Déconnexion</Link></li>
          </ul>
        </motion.div>

        {/* Colonne Contact */}
        <motion.div
          className="footer-col"
          variants={fadeInUp}
          initial="hidden"
          whileInView="visible"
          transition={{ duration: 0.8, delay: 2 }}
          viewport={{ once: false, amount: 0.3 }}
        >
          <h2 className="footer-title">Contactez-nous</h2>
          <ul className="footer-contact">
            <li>
              <FaMapMarkerAlt className="footer-icon" /> #56, Léogâne, Haïti
            </li>
            <li>
              <FaEnvelope className="footer-icon" /> collegequisqueyadeleogane@gmail.com
            </li>
            <li>
              <FaPhone className="footer-icon" /> +509 1234 5678
            </li>
          </ul>
        </motion.div>
      </div>

      {/* Bas du footer */}
      <motion.div
        className="footer-bottom"
        variants={fadeInUp}
        initial="hidden"
        whileInView="visible"
        transition={{ duration: 0.8, delay: 2.5 }}
        viewport={{ once: false, amount: 0.3 }}
      >
        <p>© 2025 Collège Quisqueya — Tous droits réservés</p>
        <ul className="footer-bottom-links">
          <li><Link to="/login">Connexion</Link></li>
          <li><Link to="/logout">Déconnexion</Link></li>
        </ul>
      </motion.div>
    </footer>
  );
}
