// frontend/src/pages/AboutPage.jsx
import { useEffect, useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import API, { BASE_URL } from "../api";
import "./aboutpage.css";
import { motion } from "framer-motion"; // ✅ Framer Motion

export function AboutPage() {
  const [aboutInfo, setAboutInfo] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [founders, setFounders] = useState([]);
  const [staff, setStaff] = useState([]);
  const [values, setValues] = useState([]);
  const [keystats, setKeyStats] = useState([]);
  const [vision, setVision] = useState([]);
  const [examResults, setExamResults] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    API.get("about/")
      .then((res) => {
        setAboutInfo(res.data.about_info);
        setTimeline(res.data.timeline || []);
        setFounders(res.data.founders || []);
        setStaff(res.data.staff || []);
        setValues(res.data.values || []);
        setKeyStats(res.data.keystats || []);
        setVision(res.data.vision || []);
        setExamResults(res.data.exam_results || []);
      })
      .catch(() => setError("Impossible de charger la page À propos."));
  }, []);

  // Variantes Framer Motion
  const fadeInUp = {
    hidden: { opacity: 0, y: 50 },
    visible: { opacity: 1, y: 0 },
  };

  const scaleUp = {
    hidden: { opacity: 0, scale: 0 },
    visible: { opacity: 1, scale: 1 },
  };

  return (
    <>
      <HeaderPage />
      <div className="about-container">
        {error && <p className="error">{error}</p>}

        {/* Hero Section */}
        {aboutInfo ? (
          <motion.section
            className="hero"
            initial="hidden"
            whileInView="visible"
            variants={fadeInUp}
            transition={{ duration: 1 }}
            viewport={{ once: false, amount: 0.3 }}
          >
            {aboutInfo.main_image && (
              <img
                src={`${BASE_URL}${aboutInfo.main_image}`}
                alt="Collège Quisqueya"
              />
            )}
            <div className="hero-text">
              <motion.h1
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                transition={{ duration: 1 }}
              >
                {aboutInfo.title}
              </motion.h1>
              <p>{aboutInfo.description}</p>
              <p className="founded">Fondé en {aboutInfo.founded_date}</p>
            </div>
          </motion.section>
        ) : (
          <p className="empty">ℹ️ Infos générales non disponibles.</p>
        )}

        {/* Timeline */}
        <motion.section
          className="section timeline"
          initial="hidden"
          whileInView="visible"
          variants={fadeInUp}
          transition={{ duration: 1 }}
          viewport={{ once: false, amount: 0.3 }}
        >
          <motion.h2
            initial="hidden"
            whileInView="visible"
            variants={scaleUp}
            transition={{ duration: 1 }}
          >
            Notre Histoire
          </motion.h2>
          {timeline.length > 0 ? (
            <div className="timeline-grid">
              {timeline.map((event, idx) => (
                <motion.div
                  key={event.id}
                  className={`timeline-item ${idx % 2 === 0 ? "left" : "right"}`}
                  initial={{ opacity: 0, x: idx % 2 === 0 ? -100 : 100 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 1 }}
                  viewport={{ once: false, amount: 0.3 }}
                >
                  <h3>{event.year}</h3>
                  <p className="timeline-title">{event.title}</p>
                  <p>{event.description}</p>
                  {event.image && (
                    <img
                      src={`${BASE_URL}${event.image}`}
                      alt={event.title}
                    />
                  )}
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun événement historique enregistré.</p>
          )}
        </motion.section>

        {/* Fondateurs */}
        <motion.section
          className="section founders"
          initial="hidden"
          whileInView="visible"
          variants={fadeInUp}
          transition={{ duration: 1 }}
          viewport={{ once: false, amount: 0.3 }}
        >
          <motion.h2
            initial="hidden"
            whileInView="visible"
            variants={scaleUp}
            transition={{ duration: 1 }}
          >
            Les Fondateurs
          </motion.h2>
          {founders.length > 0 ? (
            <div className="grid">
              {founders.map((f) => (
                <motion.div
                  key={f.id}
                  className="card"
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8 }}
                  viewport={{ once: false, amount: 0.3 }}
                >
                  {f.photo && (
                    <img
                      src={`${BASE_URL}${f.photo}`}
                      alt={f.name}
                    />
                  )}
                  <h3>{f.name}</h3>
                  <p className="role">{f.role}</p>
                  <p>{f.bio}</p>
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun fondateur enregistré.</p>
          )}
        </motion.section>

        {/* Staff */}
        <motion.section
          className="section staff"
          initial="hidden"
          whileInView="visible"
          variants={fadeInUp}
          transition={{ duration: 1 }}
          viewport={{ once: false, amount: 0.3 }}
        >
          <motion.h2 variants={scaleUp}>Notre Équipe</motion.h2>
          {staff.length > 0 ? (
            <div className="grid">
              {staff.map((s) => (
                <motion.div
                  key={s.id}
                  className="card"
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8 }}
                >
                  {s.photo && (
                    <img
                      src={`${BASE_URL}${s.photo}`}
                      alt={s.name}
                    />
                  )}
                  <h3>{s.name}</h3>
                  <p className="role">{s.role}</p>
                  <p>{s.bio}</p>
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun membre du personnel enregistré.</p>
          )}
        </motion.section>

        {/* Valeurs */}
        <motion.section className="section values" initial="hidden" whileInView="visible" variants={fadeInUp}>
          <motion.h2 variants={scaleUp}>Nos Valeurs</motion.h2>
          {values.length > 0 ? (
            <div className="grid">
              {values.map((v) => (
                <motion.div
                  key={v.id}
                  className="card value-card"
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8 }}
                >
                  <h3>{v.title}</h3>
                  <p>{v.description}</p>
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucune valeur enregistrée.</p>
          )}
        </motion.section>

        {/* Stats */}
        <motion.section className="section keystats" initial="hidden" whileInView="visible" variants={fadeInUp}>
          <motion.h2 variants={scaleUp}>Quelques Chiffres</motion.h2>
          {keystats.length > 0 ? (
            <div className="grid">
              {keystats.map((k) => (
                <motion.div
                  key={k.id}
                  className="stat-card"
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.8 }}
                >
                  <h3>{k.value}</h3>
                  <p>{k.label}</p>
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun chiffre clé enregistré.</p>
          )}
        </motion.section>

        {/* Vision */}
        <motion.section className="section vision" initial="hidden" whileInView="visible" variants={fadeInUp}>
          <motion.h2 variants={scaleUp}>Notre Vision</motion.h2>
          {vision.length > 0 ? (
            vision.map((v) => (
              <motion.div
                key={v.id}
                className="vision-card"
                initial={{ opacity: 0, x: -80 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 1 }}
              >
                {v.image && (
                  <img
                    src={`${BASE_URL}${v.image}`}
                    alt={v.title}
                  />
                )}
                <div>
                  <h3>{v.title}</h3>
                  <p>{v.description}</p>
                </div>
              </motion.div>
            ))
          ) : (
            <p className="empty">ℹ️ Aucune vision enregistrée.</p>
          )}
        </motion.section>

        {/* Exam Results */}
        <motion.section className="section exams" initial="hidden" whileInView="visible" variants={fadeInUp}>
          <motion.h2 variants={scaleUp}>Résultats Académiques</motion.h2>
          {examResults.length > 0 ? (
            <div className="grid">
              {examResults.map((e) => (
                <motion.div
                  key={e.id}
                  className="exam-card"
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8 }}
                >
                  <h3>{e.exam_name}</h3>
                  <p>{e.success_rate}% de réussite</p>
                  <p>{e.total_students} élèves déjà réussis</p>
                  {e.description && <p>{e.description}</p>}
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun résultat académique enregistré.</p>
          )}
        </motion.section>
      </div>
      <FooterPage />
    </>
  );
}
