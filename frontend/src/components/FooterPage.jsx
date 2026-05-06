import { Link } from "react-router-dom";
import {
  FaMapMarkerAlt,
  FaEnvelope,
  FaPhone,
  FaFacebookF,
  FaInstagram,
  FaWhatsapp,
  FaYoutube,
} from "react-icons/fa";
import { motion } from "framer-motion";

const fadeUp = {
  hidden:  { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0 },
};

const NAV_LINKS = [
  { to: "/",          label: "Accueil" },
  { to: "/about",     label: "À propos" },
  { to: "/news",      label: "Actualités" },
  { to: "/schoollife",label: "Vie Scolaire" },
  { to: "/contact",   label: "Contact" },
  { to: "/donation",  label: "Donation" },
];

const SOCIAL = [
  { Icon: FaFacebookF, href: "#", label: "Facebook" },
  { Icon: FaInstagram, href: "#", label: "Instagram" },
  { Icon: FaWhatsapp,  href: "#", label: "WhatsApp" },
  { Icon: FaYoutube,   href: "#", label: "YouTube" },
];

const HORAIRES = [
  { jour: "Lun – Ven", heure: "7h30 – 16h00", ouvert: true },
  { jour: "Samedi",    heure: "8h00 – 12h00",  ouvert: true },
  { jour: "Dimanche",  heure: "Fermé",           ouvert: false },
];

export function FooterPage() {
  return (
    <footer className="bg-navy text-white">

      {/* Barre accent dorée */}
      <div className="h-1 bg-gradient-to-r from-navy via-gold to-navy" />

      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-10">

          {/* ── Col 1 : Présentation + réseaux ─────────────────────────────── */}
          <motion.div
            variants={fadeUp}
            initial="hidden"
            whileInView="visible"
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: false, amount: 0.3 }}
          >
            <h2 className="text-base font-black text-gold mb-1 leading-tight">
              Collège Quisqueya
            </h2>
            <p className="text-white/40 text-xs mb-3">de Léogâne</p>
            <div className="w-8 h-0.5 bg-gold mb-4" />
            <p className="text-white/55 text-sm leading-relaxed">
              Établissement d'excellence fondé en 1985, nous accompagnons
              chaque élève vers la réussite grâce à un encadrement exigeant
              et bienveillant.
            </p>

            {/* Réseaux sociaux */}
            <div className="flex gap-2.5 mt-5">
              {SOCIAL.map(({ Icon, href, label }) => (
                <a
                  key={label}
                  href={href}
                  aria-label={label}
                  className="w-9 h-9 rounded-full bg-white/10 hover:bg-gold flex items-center justify-center text-white/60 hover:text-navy transition-all duration-200"
                >
                  <Icon size={13} />
                </a>
              ))}
            </div>
          </motion.div>

          {/* ── Col 2 : Navigation rapide ───────────────────────────────────── */}
          <motion.div
            variants={fadeUp}
            initial="hidden"
            whileInView="visible"
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: false, amount: 0.3 }}
          >
            <h2 className="text-xs font-bold text-white uppercase tracking-widest mb-4">
              Navigation
            </h2>
            <div className="w-8 h-0.5 bg-gold mb-4" />
            <ul className="space-y-2.5">
              {NAV_LINKS.map(({ to, label }) => (
                <li key={to}>
                  <Link
                    to={to}
                    className="group flex items-center gap-2 text-white/55 hover:text-gold text-sm transition-colors duration-200"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-gold/0 group-hover:bg-gold transition-all flex-shrink-0" />
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* ── Col 3 : Contact ──────────────────────────────────────────────── */}
          <motion.div
            variants={fadeUp}
            initial="hidden"
            whileInView="visible"
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: false, amount: 0.3 }}
          >
            <h2 className="text-xs font-bold text-white uppercase tracking-widest mb-4">
              Contactez-nous
            </h2>
            <div className="w-8 h-0.5 bg-gold mb-4" />
            <ul className="space-y-3.5">
              <li className="flex items-start gap-3 text-sm text-white/55">
                <FaMapMarkerAlt className="text-gold mt-0.5 flex-shrink-0" size={13} />
                #56 Rue Principale, Léogâne, Haïti
              </li>
              <li className="flex items-start gap-3 text-sm text-white/55">
                <FaEnvelope className="text-gold mt-0.5 flex-shrink-0" size={13} />
                <a
                  href="mailto:collegequisqueyadeleogane@gmail.com"
                  className="hover:text-gold transition-colors break-all"
                >
                  collegequisqueyadeleogane@gmail.com
                </a>
              </li>
              <li className="flex items-center gap-3 text-sm text-white/55">
                <FaPhone className="text-gold flex-shrink-0" size={13} />
                <a href="tel:+50912345678" className="hover:text-gold transition-colors">
                  +509 1234 5678
                </a>
              </li>
            </ul>
          </motion.div>

          {/* ── Col 4 : Horaires + CTA ───────────────────────────────────────── */}
          <motion.div
            variants={fadeUp}
            initial="hidden"
            whileInView="visible"
            transition={{ duration: 0.6, delay: 0.4 }}
            viewport={{ once: false, amount: 0.3 }}
          >
            <h2 className="text-xs font-bold text-white uppercase tracking-widest mb-4">
              Horaires
            </h2>
            <div className="w-8 h-0.5 bg-gold mb-4" />
            <ul className="space-y-2 mb-6">
              {HORAIRES.map(({ jour, heure, ouvert }) => (
                <li key={jour} className="flex justify-between text-sm">
                  <span className="text-white/55">{jour}</span>
                  <span className={ouvert ? "text-white/80" : "text-white/30"}>
                    {heure}
                  </span>
                </li>
              ))}
            </ul>

            <Link
              to="/contact"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-gold text-navy text-sm font-bold rounded-full hover:bg-gold-light transition-all duration-200"
            >
              Nous écrire
            </Link>
          </motion.div>
        </div>
      </div>

      {/* Bas du footer */}
      <div className="border-t border-white/10">
        <div className="max-w-6xl mx-auto px-4 py-5 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-white/35">
          <p>© {new Date().getFullYear()} Collège Quisqueya de Léogâne. Tous droits réservés.</p>
          <div className="flex gap-4">
            <Link to="/login"  className="hover:text-white/65 transition-colors">Connexion</Link>
            <span>·</span>
            <Link to="/about"  className="hover:text-white/65 transition-colors">À propos</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
