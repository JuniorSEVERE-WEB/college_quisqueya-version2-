// frontend/src/pages/NewsPage.jsx
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
  const [search, setSearch] = useState("");        // 🔹 champ recherche
  const [category, setCategory] = useState("");    // 🔹 filtre catégorie
  const [page, setPage] = useState(1);             // 🔹 numéro de page actuelle
  const [hasMore, setHasMore] = useState(true);    // 🔹 s’il reste des articles

  const getImageUrl = (img) => {
    if (!img) return "";
    if (/^https?:\/\//i.test(img)) return img;
    const base = API?.defaults?.baseURL || "";
    const root = base.replace(/\/api\/?.*$/, "");
    return `${root}${img.startsWith("/") ? "" : "/"}${img}`;
  };

  // 🔹 Charger les articles
  const fetchArticles = async (pageNum = 1, append = false) => {
    try {
      setLoading(true);
      const res = await API.get("blog/articles/", {
        params: {
          is_published: true,
          ordering: "-date_published",
          page: pageNum,
          page_size: 6,   // 6 articles par page
          search: search || undefined,
          category: category || undefined,
        },
      });

      const data = Array.isArray(res.data) ? res.data : res.data?.results || [];

      if (append) {
        setArticles((prev) => [...prev, ...data]);
      } else {
        setArticles(data);
      }

      setHasMore(!!res.data?.next); // ✅ vérifier s’il reste des pages
      setError("");
    } catch (e) {
      setError("Impossible de charger les actualités.");
      setHasMore(false);
    } finally {
      setLoading(false);
    }
  };

  // 🔹 Charger les articles quand search/category changent
  useEffect(() => {
    setPage(1); // reset page
    fetchArticles(1, false);
  }, [search, category]);

  // 🔹 Charger plus d’articles
  const loadMore = () => {
    const nextPage = page + 1;
    fetchArticles(nextPage, true);
    setPage(nextPage);
  };

  return (
    <>
      <HeaderPage />

      <div className="news-page">
        <h2>Actualités</h2>

        {/* 🔹 Barre de recherche + Catégories */}
        <div className="news-filters">
          <input
            type="text"
            placeholder="Rechercher un article..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="news-search"
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="news-category"
          >
            <option value="">Toutes catégories</option>
            <option value="politique">Politique</option>
            <option value="genie">Génie</option>
            <option value="sport">Sport</option>
            <option value="education">Éducation</option>
            <option value="technologie">Technologie</option>
            <option value="metier">Métier professionnel</option>
            <option value="divertissement">Divertissement</option>
          </select>
        </div>

        {loading && articles.length === 0 && <div>Chargement des actualités…</div>}
        {!loading && error && <div>{error}</div>}
        {!loading && !error && articles.length === 0 && <div>Aucun article pour le moment.</div>}

        {!loading && !error && articles.length > 0 && (
          <>
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
                      {new Date(
                        a.date_published || a.published_at || a.created_at
                      ).toLocaleDateString("fr-FR")}{" "}
                      par {a.author?.username || a.author_name || "l'Admin"}
                    </div>
                    <h3 className="news-title">{a.title}</h3>
                    <p className="news-desc">
                      {(a.description || a.content || "").slice(0, 150)}
                      {(a.description || a.content || "").length > 150 ? "…" : ""}
                    </p>
                    <div className="news-actions">
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

            {/* 🔹 Bouton "Plus d’articles" */}
            {hasMore && (
              <div className="news-load-more">
                <button onClick={loadMore} className="btn-load-more">
                  Plus d’articles
                </button>
              </div>
            )}
          </>
        )}
      </div>

      <FooterPage />
    </>
  );
}
