// frontend/src/pages/SchoolLife.jsx
import { useEffect, useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import API from "../api";
import "./schoollife.css";

export function SchoolLife() {
  const [clubs, setClubs] = useState([]);
  const [events, setEvents] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [gallery, setGallery] = useState([]);
  const [error, setError] = useState("");

  // Charger données
  useEffect(() => {
    API.get("schoollife/clubs/")
      .then((res) => setClubs(res.data.results || res.data))
      .catch(() => setError("Impossible de charger les clubs."));

    API.get("schoollife/events/")
      .then((res) => setEvents(res.data.results || res.data))
      .catch(() => setError("Impossible de charger les événements."));

    API.get("schoollife/testimonials/")
      .then((res) => setTestimonials(res.data.results || res.data))
      .catch(() => setError("Impossible de charger les témoignages."));

    API.get("schoollife/gallery/")
      .then((res) => setGallery(res.data.results || res.data))
      .catch(() => setError("Impossible de charger la galerie."));
  }, []);

  // 🎨 Animation au scroll (comme HomePage.jsx)
  useEffect(() => {
    const reveals = document.querySelectorAll(".reveal");

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("active");
          } else {
            // ✅ Permet de rejouer l'animation si on remonte/redescend
            entry.target.classList.remove("active");
          }
        });
      },
      { threshold: 0.15 }
    );

    reveals.forEach((el) => observer.observe(el));
    return () => reveals.forEach((el) => observer.unobserve(el));
  }, [clubs, events, testimonials, gallery]);

  return (
    <>
      <HeaderPage />
      <div className="schoollife-container">
        <h1 className="title reveal">🌟 Vie Scolaire</h1>
        {error && <p className="error">{error}</p>}

        {/* Clubs */}
        <section className="section reveal">
          <h2>Nos Clubs</h2>
          <div className="grid">
            {clubs.map((club) => (
              <div key={club.id} className="card">
                <h3>{club.name}</h3>
                <p>{club.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Événements */}
        <section className="section reveal">
          <h2>Événements</h2>
          <div className="grid">
            {events.map((event) => (
              <div key={event.id} className="card">
                <h3>{event.title}</h3>
                <p>{event.description}</p>
                <p className="date">📅 {event.date}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Témoignages */}
        <section className="section reveal">
          <h2>Témoignages</h2>
          <div className="grid">
            {testimonials.map((t) => (
              <div key={t.id} className="card">
                {t.photo && (
                  <img
                    src={t.photo}
                    alt={t.name}
                    className="testimonial-photo"
                  />
                )}
                <blockquote>{t.message}</blockquote>
                <p className="author">
                  — {t.name} {t.role && `(${t.role})`}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Galerie */}
        <section className="section reveal">
          <h2>Galerie</h2>
          <div className="grid gallery">
            {gallery.map((g) => (
              <div key={g.id} className="gallery-item">
                <img src={g.image} alt={g.title} />
                <p>{g.title}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
      <FooterPage />
    </>
  );
}
