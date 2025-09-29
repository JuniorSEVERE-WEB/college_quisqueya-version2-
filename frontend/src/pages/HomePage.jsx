import { useEffect, useState } from 'react';
import { HeaderPage } from '../components/HeaderPage';
import { FooterPage } from '../components/FooterPage';
import './homepage.css';
import API from '../api';

export function HomePage() {
  const [slides, setSlides] = useState([]);
  const [current, setCurrent] = useState(0);
  const [welcome, setWelcome] = useState(null);
  const [values, setValues] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // 🔹 États pour l'animation typewriter
  const [titleIndex, setTitleIndex] = useState(0); // index du mot
  const [charIndex, setCharIndex] = useState(0); // index de la lettre
  const [displayedText, setDisplayedText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  // Charger les données
  useEffect(() => {
    async function fetchData() {
      try {
        const [slidesRes, welcomeRes, valuesRes] = await Promise.all([
          API.get('homepage/slides/'),
          API.get('homepage/welcome/'),
          API.get('homepage/values/')
        ]);

        setSlides(slidesRes.data.results || slidesRes.data || []);
        setWelcome(
          Array.isArray(welcomeRes.data) ? welcomeRes.data[0] : welcomeRes.data
        );
        setValues(valuesRes.data.results || valuesRes.data || []);
        setError('');
      } catch (err) {
        console.error('Erreur chargement homepage:', err);
        setError("Impossible de charger la page d’accueil.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // Effet machine à écrire
  useEffect(() => {
    if (slides.length === 0) return;

    const titles = slides[current]?.titles || [];
    if (titles.length === 0) return;

    const currentTitle = titles[titleIndex]?.title || '';

    let timeout;

    if (!isDeleting && charIndex < currentTitle.length) {
      // Écrire le mot lettre par lettre
      timeout = setTimeout(() => {
        setDisplayedText(currentTitle.substring(0, charIndex + 1));
        setCharIndex(charIndex + 1);
      }, 120);
    } else if (!isDeleting && charIndex === currentTitle.length) {
      // Pause avant de supprimer
      timeout = setTimeout(() => setIsDeleting(true), 1200);
    } else if (isDeleting && charIndex > 0) {
      // Effacer le mot lettre par lettre
      timeout = setTimeout(() => {
        setDisplayedText(currentTitle.substring(0, charIndex - 1));
        setCharIndex(charIndex - 1);
      }, 80);
    } else if (isDeleting && charIndex === 0) {
      // Passer au mot suivant
      setIsDeleting(false);
      setTitleIndex((prev) => (prev + 1) % titles.length);
    }

    return () => clearTimeout(timeout);
  }, [charIndex, isDeleting, titleIndex, slides, current]);

  // Navigation carrousel
  const prev = () =>
    setCurrent((c) =>
      slides.length > 0 ? (c - 1 + slides.length) % slides.length : 0
    );
  const next = () =>
    setCurrent((c) => (slides.length > 0 ? (c + 1) % slides.length : 0));

  // Construire URL images
  const getImageUrl = (img) => {
    if (!img) return '';
    if (/^https?:\/\//i.test(img)) return img;
    const base = API?.defaults?.baseURL || '';
    const root = base.replace(/\/api\/?.*$/, ''); 
    return `${root}${img.startsWith('/') ? '' : '/'}${img}`;
  };

  return (
    <>
      <HeaderPage />

      {loading && <div className="loading">Chargement…</div>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && (
        <>
          {/* Carrousel */}
          {slides.length > 0 && (
            <div className="carroussel">
              <div
                className="carroussel-img"
                style={{
                  backgroundImage: `url(${getImageUrl(slides[current].image)})`,
                }}
              >
                <div className="carroussel-overlay">
                  {/* 🔹 Titre animé */}
                  <h2 className="carroussel-titles">
                    {displayedText}
                    <span className="cursor">|</span>
                  </h2>

                  {/* Texte statique */}
                  <p className="carroussel-description">
                    {slides[current].text}
                  </p>
                </div>
              </div>

              {/* Boutons */}
              
            </div>
          )}

          {/* Section Bienvenue */}
          {welcome && (
            <section className="bienvenue-section">
              <div className="container">
                <div className="bienvenue-card">
                  <h1 className="bienvenue-title">{welcome.title}</h1>
                  <p className="bienvenue-text">{welcome.content}</p>
                </div>
              </div>
            </section>
          )}

          {/* Section Valeurs */}
          {values.length > 0 && (
            <section className="valeurs-section">
              <div className="container">
                <h2 className="valeurs-title">Nos Valeurs & Missions</h2>
                <div className="valeurs-grid">
                  {values.map((v) => (
                    <div key={v.id} className="valeur-card">
                      <div className="valeur-icon">{v.icon}</div>
                      <h3>{v.title}</h3>
                      <p>{v.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          )}
        </>
      )}

      <FooterPage />
    </>
  );
}
