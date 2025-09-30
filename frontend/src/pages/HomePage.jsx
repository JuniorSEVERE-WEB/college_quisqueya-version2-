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
  const [articles, setArticles] = useState([]); // 🔹 Nouvel état pour articles

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // 🔹 États pour l'animation typewriter
  const [titleIndex, setTitleIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  // Charger les données
  useEffect(() => {
    async function fetchData() {
      try {
        const [slidesRes, welcomeRes, valuesRes, articlesRes] = await Promise.all([
          API.get('homepage/slides/'),
          API.get('homepage/welcome/'),
          API.get('homepage/values/'),
          API.get('blog/articles/?is_published=true') // 🔹 Récupère articles publiés
        ]);

        setSlides(slidesRes.data.results || slidesRes.data || []);
        setWelcome(
          welcomeRes.data.results
            ? welcomeRes.data.results[0]
            : (Array.isArray(welcomeRes.data) ? welcomeRes.data[0] : welcomeRes.data)
        );
        setValues(valuesRes.data.results || valuesRes.data || []);
        setArticles(articlesRes.data.results || articlesRes.data || []); // 🔹 Enregistre articles
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
      timeout = setTimeout(() => {
        setDisplayedText(currentTitle.substring(0, charIndex + 1));
        setCharIndex(charIndex + 1);
      }, 120);
    } else if (!isDeleting && charIndex === currentTitle.length) {
      timeout = setTimeout(() => setIsDeleting(true), 1200);
    } else if (isDeleting && charIndex > 0) {
      timeout = setTimeout(() => {
        setDisplayedText(currentTitle.substring(0, charIndex - 1));
        setCharIndex(charIndex - 1);
      }, 80);
    } else if (isDeleting && charIndex === 0) {
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
                  <p className="carroussel-description">
                    {slides[current].text}
                  </p>
                </div>
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

          {/* 🔹 Section Articles */}
          {articles.length > 0 && (
            <section className="articles-home">
              <div className="container">
                <h2>Actualités & Articles</h2>

                {/* Grille Desktop */}
                <div className="articles-grid">
                  {articles.slice(0, 4).map((a) => (
                    <div key={a.id} className="article-card">
                      <div
                        className="article-card-img"
                        style={{ backgroundImage: `url(${getImageUrl(a.image)})` }}
                      />
                      <div className="article-card-body">
                        <div className="article-meta">
                          {new Date(a.date_published).toLocaleDateString("fr-FR")}
                        </div>
                        <h3 className="article-title">{a.title}</h3>
                        <p className="article-desc">
                          {a.description.length > 120
                            ? a.description.substring(0, 120) + "..."
                            : a.description}
                        </p>
                        <a href={`/news/${a.id}`} className="btn-read">
                          Lire plus
                        </a>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Carrousel Mobile (simple version) */}
                <div className="articles-carousel">
                  {articles.slice(0, 4).map((a) => (
                    <div key={a.id} className="article-card">
                      <div
                        className="article-card-img"
                        style={{ backgroundImage: `url(${getImageUrl(a.image)})` }}
                      />
                      <div className="article-card-body">
                        <div className="article-meta">
                          {new Date(a.date_published).toLocaleDateString("fr-FR")}
                        </div>
                        <h3 className="article-title">{a.title}</h3>
                        <p className="article-desc">
                          {a.description.length > 120
                            ? a.description.substring(0, 120) + "..."
                            : a.description}
                        </p>
                        <a href={`/news/${a.id}`} className="btn-read">
                          Lire plus
                        </a>
                      </div>
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
