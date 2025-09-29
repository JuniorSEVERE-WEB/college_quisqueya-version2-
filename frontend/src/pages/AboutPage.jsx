// frontend/src/pages/AboutPage.jsx
import { useEffect, useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import API, { BASE_URL } from "../api";  // ✅ import BASE_URL
import "./aboutpage.css";

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

  // 🎨 Animations au scroll
  useEffect(() => {
    const reveals = document.querySelectorAll(".reveal");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("active");
          }
        });
      },
      { threshold: 0.1 }
    );

    reveals.forEach((el) => observer.observe(el));
    return () => reveals.forEach((el) => observer.unobserve(el));
  }, [timeline, founders, staff, values, keystats, vision, examResults]);

  return (
    <>
      <HeaderPage />
      <div className="about-container">
        {error && <p className="error">{error}</p>}

        {/* Hero Section */}
        {aboutInfo ? (
          <section className="hero reveal">
            {aboutInfo.main_image && (
              <img
                src={`${BASE_URL}${aboutInfo.main_image}`} // ✅ correction
                alt="Collège Quisqueya"
              />
            )}
            <div className="hero-text">
              <h1>{aboutInfo.title}</h1>
              <p>{aboutInfo.description}</p>
              <p className="founded">Fondé en {aboutInfo.founded_date}</p>
            </div>
          </section>
        ) : (
          <p className="empty">ℹ️ Infos générales non disponibles.</p>
        )}

        {/* Timeline */}
        <section className="section timeline">
          <h2>Notre Histoire</h2>
          {timeline.length > 0 ? (
            <div className="timeline-grid">
              {timeline.map((event) => (
                <div key={event.id} className="timeline-item reveal">
                  <h3>{event.year}</h3>
                  <p className="timeline-title">{event.title}</p>
                  <p>{event.description}</p>
                  {event.image && (
                    <img
                      src={`${BASE_URL}${event.image}`} // ✅ correction
                      alt={event.title}
                    />
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun événement historique enregistré.</p>
          )}
        </section>

        {/* Founders */}
        <section className="section founders">
          <h2>Les Fondateurs</h2>
          {founders.length > 0 ? (
            <div className="grid">
              {founders.map((f) => (
                <div key={f.id} className="card reveal">
                  {f.photo && (
                    <img
                      src={`${BASE_URL}${f.photo}`} // ✅ correction
                      alt={f.name}
                    />
                  )}
                  <h3>{f.name}</h3>
                  <p className="role">{f.role}</p>
                  <p>{f.bio}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun fondateur enregistré.</p>
          )}
        </section>

        {/* Staff */}
        <section className="section staff">
          <h2>Notre Équipe</h2>
          {staff.length > 0 ? (
            <div className="grid">
              {staff.map((s) => (
                <div key={s.id} className="card reveal">
                  {s.photo && (
                    <img
                      src={`${BASE_URL}${s.photo}`} // ✅ correction
                      alt={s.name}
                    />
                  )}
                  <h3>{s.name}</h3>
                  <p className="role">{s.role}</p>
                  <p>{s.bio}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun membre du personnel enregistré.</p>
          )}
        </section>

        {/* Values */}
        <section className="section values">
          <h2>Nos Valeurs</h2>
          {values.length > 0 ? (
            <div className="grid">
              {values.map((v) => (
                <div key={v.id} className="card value-card reveal">
                  <h3>{v.title}</h3>
                  <p>{v.description}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucune valeur enregistrée.</p>
          )}
        </section>

        {/* Key Stats */}
        <section className="section keystats">
          <h2>Quelques Chiffres</h2>
          {keystats.length > 0 ? (
            <div className="grid">
              {keystats.map((k) => (
                <div key={k.id} className="stat-card reveal">
                  <h3>{k.value}</h3>
                  <p>{k.label}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun chiffre clé enregistré.</p>
          )}
        </section>

        {/* Vision */}
        <section className="section vision">
          <h2>Notre Vision</h2>
          {vision.length > 0 ? (
            vision.map((v) => (
              <div key={v.id} className="vision-card reveal">
                {v.image && (
                  <img
                    src={`${BASE_URL}${v.image}`} // ✅ correction
                    alt={v.title}
                  />
                )}
                <div>
                  <h3>{v.title}</h3>
                  <p>{v.description}</p>
                </div>
              </div>
            ))
          ) : (
            <p className="empty">ℹ️ Aucune vision enregistrée.</p>
          )}
        </section>

        {/* Exam Results */}
        <section className="section exams">
          <h2>Résultats Académiques</h2>
          {examResults.length > 0 ? (
            <div className="grid">
              {examResults.map((e) => (
                <div key={e.id} className="exam-card reveal">
                  <h3>{e.exam_name}</h3>
                  <p>{e.success_rate}% de réussite</p>
                  <p>{e.total_students} élèves déjà réussis</p>
                  {e.description && <p>{e.description}</p>}
                </div>
              ))}
            </div>
          ) : (
            <p className="empty">ℹ️ Aucun résultat académique enregistré.</p>
          )}
        </section>
      </div>
      <FooterPage />
    </>
  );
}
