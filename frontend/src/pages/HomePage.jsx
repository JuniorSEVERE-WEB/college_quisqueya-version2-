import { useEffect, useState } from 'react';
import { HeaderPage } from '../components/HeaderPage';
import './homepage.css';
import { FooterPage } from '../components/FooterPage';
import { Link } from 'react-router-dom';

import API from '../api';

const slides = [
  {
    image: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
    text: 'Bienvenue à Quisqueya!'
  },
  {
    image: 'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=800&q=80',
    text: 'Découvrez nos programmes éducatifs.'
  },
  {
    image: 'https://images.unsplash.com/photo-1513258496099-48168024aec0?auto=format&fit=crop&w=800&q=80',
    text: 'Rejoignez une communauté dynamique.'
  }
];

export function HomePage() {
  const [current, setCurrent] = useState(0);
  const [articles, setArticles] = useState([]);
  const [newsIndex, setNewsIndex] = useState(0);
  const [loadingNews, setLoadingNews] = useState(true);   // + état chargement
  const [errorNews, setErrorNews] = useState(''); 

  useEffect(() => {
    console.log('API baseURL =', API?.defaults?.baseURL);
    API.get('blog/articles/', {
      params: { is_published: true, ordering: '-date_published', page_size: 4 }
    })
      .then(res => {
        const data = Array.isArray(res.data) ? res.data : (res.data?.results || []);
        setArticles(data.slice(0, 4));
        setNewsIndex(0);
        setErrorNews('');
      })
      .catch(err => {
        console.error('Erreur chargement articles', err);
        setArticles([]);
        setErrorNews("Impossible de charger les actualités.");
      })
      .finally(() => setLoadingNews(false));
  }, []);

  useEffect(() => {
    if (articles.length < 2) return;
    const t = setInterval(() => setNewsIndex(i => (i + 1) % articles.length), 5000);
    return () => clearInterval(t);
  }, [articles]);

  const prev = () => setCurrent(c => (c - 1 + slides.length) % slides.length);
  const next = () => setCurrent(c => (c + 1) % slides.length);

  const prevNews = () => setNewsIndex(i => (i - 1 + articles.length) % articles.length);
  const nextNews = () => setNewsIndex(i => (i + 1) % articles.length);

  const getImageUrl = (img) => {
    if (!img) return '';
    if (/^https?:\/\//i.test(img)) return img;
    const base = API?.defaults?.baseURL || '';
    const root = base.replace(/\/api\/?.*$/, ''); // http://127.0.0.1:8000
    return `${root}${img.startsWith('/') ? '' : '/'}${img}`;
  };

  return (
    <>
      <HeaderPage />

      {/* Carrousel */}
      <div className="carroussel">
        <div className="carroussel-img" style={{ backgroundImage: `url(${slides[current].image})` }}>
          <div className="carroussel-text">{slides[current].text}</div>
          <button className="carroussel-btn prev" onClick={prev}>&lt;</button>
          <button className="carroussel-btn next" onClick={next}>&gt;</button>
        </div>
      </div>

      {/* Section Bienvenue */}
      <section className="bienvenue-section">
        <div className="container">
          <div className="bienvenue-card">
            <h1 className="bienvenue-title">Bienvenue au Collège Quisqueya de Leogane</h1>
            <p className="bienvenue-text">
              Le Collège Quisqueya est un établissement d’enseignement moderne et
              dynamique, engagé à offrir à chaque élève un cadre éducatif stimulant
              et bienveillant. Nous formons des citoyens responsables, créatifs et
              ouverts sur le monde, en alliant rigueur académique et développement
              personnel.
              <br />
              Notre mission est de cultiver l’excellence, la discipline et l’éthique,
              afin que chaque apprenant puisse s’épanouir et réaliser son plein
              potentiel.
            </p>
          </div>
        </div>
      </section>

      {/* Section Nos Valeurs / Missions */}
      <section className="valeurs-section">
        <div className="container">
          <h2 className="valeurs-title">Nos Valeurs & Missions</h2>
          <div className="valeurs-grid">
            <div className="valeur-card">
              <div className="valeur-icon">🎯</div>
              <h3>Mission</h3>
              <p>
                Offrir une éducation de qualité qui allie rigueur académique,
                innovation pédagogique et accompagnement personnalisé.
              </p>
            </div>
            <div className="valeur-card">
              <div className="valeur-icon">👁️</div>
              <h3>Vision</h3>
              <p>
                Former des leaders responsables, créatifs et ouverts sur le monde,
                capables de contribuer positivement à leur communauté.
              </p>
            </div>
            <div className="valeur-card">
              <div className="valeur-icon">🌟</div>
              <h3>Valeurs</h3>
              <p>
                Discipline, respect, solidarité et excellence. Ces valeurs reflètent
                l’esprit du Collège Quisqueya.
              </p>
            </div>
            <div className="valeur-card">
              <div className="valeur-icon">🤝</div>
              <h3>Engagement</h3>
              <p>
                Encourager la participation active à la vie de l’école et le service
                à la communauté à travers clubs, projets citoyens et partenariats locaux.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Section Actualités */}

       <div className="articles-home">
        <h2>Actualités</h2>
        {loadingNews && <div>Chargement des actualités…</div>}
        {(!loadingNews && errorNews) && <div>{errorNews}</div>}
        {(!loadingNews && !errorNews && articles.length === 0) && <div>Aucun article pour le moment!</div>}

        {/* Carrousel pour mobile/tablette */}
        {(!loadingNews && !errorNews && articles.length > 0) && (
          <div className="articles-grid">
            {articles.map((a, idx) => (
              <div key={a.id || a.slug || idx} className="article-card">
                <div
                  className="article-card-img"
                  style={{ backgroundImage: `url(${getImageUrl(a.image)})` }}
                />
                <div className="article-card-body">
                  <div className="article-meta">
                    Posté le {new Date(a.date_published || a.published_at || a.created_at).toLocaleDateString('fr-FR')}
                    {' '}par {a.author?.username || a.author_name || "l'Admin"}
                  </div>
                  <h3 className="article-title">{a.title}</h3>
                  <p className="article-desc">
                    {(a.description || a.content || '').slice(0, 120)}
                    {(a.description || a.content || '').length > 120 ? '…' : ''}
                  </p>
                  <div className="article-actions">
                    <Link
                      to={`/news/${a.slug || a.id}`}
                      className="btn-read"
                      aria-label={`Lire l’article: ${a.title}`}
                    >
                      Lire l’article
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Grille 4 cartes pour grand écran */}
        
      </div>
      <FooterPage />
      
    </>
  );
}