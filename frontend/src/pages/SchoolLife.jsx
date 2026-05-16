// frontend/src/pages/SchoolLife.jsx
import { useEffect, useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import API from "../api";
import { getMediaUrl } from "../utils/media";
import "./schoollife.css";

function EmptyState({ label }) {
  return <div className="sl-empty">{label}</div>;
}

export function SchoolLife() {
  const [clubs, setClubs] = useState([]);
  const [events, setEvents] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [gallery, setGallery] = useState([]);
  const [error, setError] = useState("");
  const [authorized, setAuthorized] = useState(false);
  const [role] = useState(localStorage.getItem("role") || "");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("⛔ Veuillez vous connecter pour accéder à la vie scolaire.");
      return;
    }

    if (["admin", "abonne", "student", "professor"].includes(role)) {
      setAuthorized(true);
    } else {
      setError(
        "Votre compte est en cours de validation. Si vous n'êtes pas étudiant ou professeur, abonnez-vous pour accéder à la vie scolaire."
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
  }, [clubs, events, testimonials, gallery, authorized]);

  return (
    <>
      <HeaderPage />

      <div className="schoollife-page">
        <section className="sl-hero">
          <div className="sl-hero-inner reveal">
            <span className="sl-hero-eyebrow">Collège Quisqueya</span>
            <h1 className="sl-hero-title">Vie Scolaire</h1>
            <p className="sl-hero-subtitle">
              Découvrez nos clubs, événements et la voix de notre communauté.
            </p>
          </div>
        </section>

        <main className="sl-container">
          {error && !authorized && (
            <div className="sl-notice">
              <span className="sl-notice-icon">ℹ️</span>
              <p>{error}</p>
            </div>
          )}

          {authorized && (
            <>
              {/* Clubs */}
              <section className="sl-section reveal">
                <header className="sl-section-header">
                  <span className="sl-section-tag">01 — Communauté</span>
                  <h2>Nos Clubs</h2>
                  <p>L'expression de la curiosité et de la passion des élèves.</p>
                </header>

                {clubs.length === 0 ? (
                  <EmptyState label="Aucun club à afficher pour l'instant." />
                ) : (
                  <div className="sl-grid sl-grid-clubs">
                    {clubs.map((club) => (
                      <article key={club.id} className="sl-card sl-card-club">
                        {club.photo && (
                          <div className="sl-card-media">
                            <img
                              src={getMediaUrl(club.photo)}
                              alt={club.name}
                              loading="lazy"
                            />
                          </div>
                        )}
                        <div className="sl-card-body">
                          <h3>{club.name}</h3>
                          <p>{club.description}</p>
                        </div>
                      </article>
                    ))}
                  </div>
                )}
              </section>

              {/* Événements */}
              <section className="sl-section reveal">
                <header className="sl-section-header">
                  <span className="sl-section-tag">02 — Calendrier</span>
                  <h2>Événements</h2>
                  <p>Le calendrier qui anime nos couloirs et notre campus.</p>
                </header>

                {events.length === 0 ? (
                  <EmptyState label="Aucun événement à venir pour le moment." />
                ) : (
                  <div className="sl-grid sl-grid-events">
                    {events.map((event) => (
                      <article key={event.id} className="sl-card sl-card-event">
                        {event.logo && (
                          <div className="sl-event-logo">
                            <img
                              src={getMediaUrl(event.logo)}
                              alt={event.title}
                              loading="lazy"
                            />
                          </div>
                        )}
                        <div className="sl-card-body">
                          <h3>{event.title}</h3>
                          <p>{event.description}</p>
                          {event.date && (
                            <span className="sl-date">📅 {event.date}</span>
                          )}
                        </div>
                      </article>
                    ))}
                  </div>
                )}
              </section>

              {/* Témoignages */}
              <section className="sl-section reveal">
                <header className="sl-section-header">
                  <span className="sl-section-tag">03 — Voix</span>
                  <h2>Témoignages</h2>
                  <p>Les mots de celles et ceux qui font Quisqueya.</p>
                </header>

                {testimonials.length === 0 ? (
                  <EmptyState label="Pas encore de témoignages publiés." />
                ) : (
                  <div className="sl-grid sl-grid-testimonials">
                    {testimonials.map((t) => (
                      <article key={t.id} className="sl-testimonial">
                        <span className="sl-quote-mark">&ldquo;</span>
                        <blockquote>{t.message}</blockquote>
                        <div className="sl-testimonial-author">
                          {t.photo && (
                            <img
                              src={getMediaUrl(t.photo)}
                              alt={t.name}
                              loading="lazy"
                            />
                          )}
                          <div>
                            <p className="sl-author-name">{t.name}</p>
                            {t.role && (
                              <p className="sl-author-role">{t.role}</p>
                            )}
                          </div>
                        </div>
                      </article>
                    ))}
                  </div>
                )}
              </section>

              {/* Galerie */}
              <section className="sl-section reveal">
                <header className="sl-section-header">
                  <span className="sl-section-tag">04 — Souvenirs</span>
                  <h2>Galerie</h2>
                  <p>Quelques instants capturés au cœur de la vie scolaire.</p>
                </header>

                {gallery.length === 0 ? (
                  <EmptyState label="La galerie est vide pour l'instant." />
                ) : (
                  <div className="sl-gallery">
                    {gallery.map((g) => (
                      <figure key={g.id} className="sl-gallery-item">
                        <img
                          src={getMediaUrl(g.image)}
                          alt={g.title}
                          loading="lazy"
                        />
                        {g.title && <figcaption>{g.title}</figcaption>}
                      </figure>
                    ))}
                  </div>
                )}
              </section>
            </>
          )}
        </main>
      </div>

      <FooterPage />
    </>
  );
}
