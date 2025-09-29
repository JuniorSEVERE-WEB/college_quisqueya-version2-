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

  // Récupérer les données du backend
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

  // Carrousel navigation
  const prev = () =>
    setCurrent(c => (slides.length > 0 ? (c - 1 + slides.length) % slides.length : 0));
  const next = () =>
    setCurrent(c => (slides.length > 0 ? (c + 1) % slides.length : 0));

  // Construire l’URL des images (backend -> frontend)
  const getImageUrl = img => {
    if (!img) return '';
    if (/^https?:\/\//i.test(img)) return img;
    const base = API?.defaults?.baseURL || '';
    const root = base.replace(/\/api\/?.*$/, ''); // ex: http://127.0.0.1:8000
    return `${root}${img.startsWith('/') ? '' : '/'}${img}`;
  };

  return (
    <>
      <HeaderPage />

      {loading && <div className="loading">Chargement…</div>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && (
        <>
          {/* Carrousel dynamique */}
          {slides.length > 0 && (
            <div className="carroussel">
              <div
                className="carroussel-img"
                style={{ backgroundImage: `url(${getImageUrl(slides[current].image)})` }}
              >
                <div className="carroussel-text">{slides[current].text}</div>
                
              </div>
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

          {/* Section Valeurs & Missions */}
          {values.length > 0 && (
            <section className="valeurs-section">
              <div className="container">
                <h2 className="valeurs-title">Nos Valeurs & Missions</h2>
                <div className="valeurs-grid">
                  {values.map(v => (
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
