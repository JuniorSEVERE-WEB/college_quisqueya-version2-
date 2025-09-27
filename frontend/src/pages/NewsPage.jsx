import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../api";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import "./newspage.css";

export default function NewsPage() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const getImageUrl = (img) => {
    if (!img) return "";
    if (/^https?:\/\//i.test(img)) return img;
    const base = API?.defaults?.baseURL || "";
    const root = base.replace(/\/api\/?.*$/, "");
    return `${root}${img.startsWith("/") ? "" : "/"}${img}`;
  };

  useEffect(() => {
    let canceled = false;
    async function fetchAll() {
      try {
        let url = "blog/articles/";
        const all = [];
        // Récupère toutes les pages si pagination DRF
        while (url) {
          const res = await API.get(url, {
            params: { is_published: true, ordering: "-date_published", page_size: 12 },
          });
          const data = Array.isArray(res.data) ? res.data : res.data?.results || [];
          all.push(...data);
          url = res.data?.next ? res.data.next.replace(/^https?:\/\/[^/]+\/api\//, "") : null;
        }
        if (!canceled) {
          setArticles(all);
          setError("");
        }
      } catch (e) {
        if (!canceled) {
          setArticles([]);
          setError("Impossible de charger les actualités.");
        }
      } finally {
        if (!canceled) setLoading(false);
      }
    }
    fetchAll();
    return () => { canceled = true; };
  }, []);

  return (
    <>
      <HeaderPage />

      <div className="news-page">
        <h2>Actualités</h2>

        {loading && <div>Chargement des actualités…</div>}
        {!loading && error && <div>{error}</div>}
        {!loading && !error && articles.length === 0 && <div>Aucun article pour le moment.</div>}

        {!loading && !error && articles.length > 0 && (
          <div className="news-grid">
            {articles.map((a, idx) => (
              <div key={a.id || a.slug || idx} className="news-card">
                <div
                  className="news-card-img"
                  style={{ backgroundImage: `url(${getImageUrl(a.image)})` }}
                  aria-label={a.title}
                />
                <div className="news-card-body">
                  <div className="news-meta">
                    Posté le{" "}
                    {new Date(a.date_published || a.published_at || a.created_at).toLocaleDateString("fr-FR")}{" "}
                    par {a.author?.username || a.author_name || "l'Admin"}
                  </div>
                  <h3 className="news-title">{a.title}</h3>
                  <p className="news-desc">
                    {(a.description || a.content || "").slice(0, 150)}
                    {(a.description || a.content || "").length > 150 ? "…" : ""}
                  </p>
                  <div className="news-actions">
                    <Link to={`/news/${a.slug || a.id}`} className="btn-read" aria-label={`Lire l’article: ${a.title}`}>
                      Lire l’article
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <FooterPage />
    </>
  );
}