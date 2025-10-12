// frontend/src/components/SchoolLife.jsx
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
  const [authorized, setAuthorized] = useState(false);
  const [role, setRole] = useState(localStorage.getItem("role") || "");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("⛔ Veuillez vous connecter pour accéder à la vie scolaire.");
      return;
    }

    // ✅ Autoriser admin, abonné, étudiant, professeur
    if (["admin", "abonne", "student", "prof"].includes(role)) {
      setAuthorized(true);
    } else {
      setError(
        "Votre inscription est en cours de validation. Si vous n’êtes pas étudiant ou professeur, abonnez-vous pour accéder aux informations du site."
      );
    }
  }, [role]);

  useEffect(() => {
    if (!authorized) return;

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
  }, [authorized]);

  // Animation scroll
  useEffect(() => {
    const reveals = document.querySelectorAll(".reveal");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add("active");
          else entry.target.classList.remove("active");
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

        {error && !authorized && (
          <p className="error" style={{ textAlign: "center" }}>
            {error}
          </p>
        )}

        {authorized && (
          <>
            {/* Clubs */}
            <section className="section reveal">
              <h2>Nos Clubs</h2>
              <div className="grid">
                {clubs.map((club) => (
                  <div key={club.id} className="card">
                    {club.photo && (
                      <img src={club.photo} alt={club.name} className="club-photo" />
                    )}
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
                    {event.logo && (
                      <img src={event.logo} alt={event.title} className="event-logo" />
                    )}
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
                      <img src={t.photo} alt={t.name} className="testimonial-photo" />
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
          </>
        )}
      </div>
      <FooterPage />
    </>
  );
}
