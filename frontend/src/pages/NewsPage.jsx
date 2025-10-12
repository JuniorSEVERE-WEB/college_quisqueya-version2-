// frontend/src/components/NewsPage.jsx
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
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [authorized, setAuthorized] = useState(false);
  const [role, setRole] = useState(localStorage.getItem("role") || "");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("⛔ Veuillez vous connecter pour accéder aux actualités.");
      setAuthorized(false);
      return;
    }

    // ✅ Autoriser admin, abonné, étudiant, professeur
    if (["admin", "abonne", "student", "prof"].includes(role)) {
      setAuthorized(true);
    } else {
      setError(
        "Votre compte est en cours de validation. Si vous n’êtes pas étudiant ou professeur, abonnez-vous pour lire les articles."
      );
      setAuthorized(false);
    }
  }, [role]);

  const fetchArticles = async (pageNum = 1, append = false) => {
    if (!authorized) return;
    try {
      setLoading(true);
      const res = await API.get("blog/articles/", {
        params: {
          is_published: true,
          ordering: "-date_published",
          page: pageNum,
          page_size: 6,
          search: search || undefined,
          category: category || undefined,
        },
      });

      const data = Array.isArray(res.data) ? res.data : res.data?.results || [];
      if (append) setArticles((prev) => [...prev, ...data]);
      else setArticles(data);

      setHasMore(!!res.data?.next);
      setError("");
    } catch (e) {
      setError("Impossible de charger les actualités.");
      setHasMore(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (authorized) {
      setPage(1);
      fetchArticles(1, false);
    }
  }, [authorized, search, category]);

  const loadMore = () => {
    const nextPage = page + 1;
    fetchArticles(nextPage, true);
    setPage(nextPage);
  };

  const getImageUrl = (img) => {
    if (!img) return "";
    if (/^https?:\/\//i.test(img)) return img;
    const base = API?.defaults?.baseURL || "";
    const root = base.replace(/\/api\/?.*$/, "");
    return `${root}${img.startsWith("/") ? "" : "/"}${img}`;
  };

  return (
    <>
      <HeaderPage />
      <div className="news-page">
        <h2>Actualités</h2>

        {!authorized ? (
          <div className="error" style={{ textAlign: "center" }}>
            {error}
          </div>
        ) : (
          <>
            {/* Filtres */}
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

            {loading && <div>Chargement des actualités…</div>}
            {!loading && error && <div>{error}</div>}
            {!loading && !error && articles.length === 0 && (
              <div>Aucun article pour le moment.</div>
            )}

            {!loading && !error && articles.length > 0 && (
              <>
                <div className="news-grid">
                  {articles.map((a, idx) => (
                    <div key={a.id || a.slug || idx} className="news-card">
                      <div
                        className="news-card-img"
                        style={{
                          backgroundImage: `url(${getImageUrl(a.image)})`,
                        }}
                        aria-label={a.title}
                      />
                      <div className="news-card-body">
                        <div className="news-meta">
                          Posté le{" "}
                          {new Date(
                            a.date_published || a.created_at
                          ).toLocaleDateString("fr-FR")}{" "}
                          par {a.author?.username || "l'Admin"}
                        </div>
                        <h3 className="news-title">{a.title}</h3>
                        <p className="news-desc">
                          {(a.description || "").slice(0, 150)}
                          {(a.description || "").length > 150 ? "…" : ""}
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

                {hasMore && (
                  <div className="news-load-more">
                    <button onClick={loadMore} className="btn-load-more">
                      Plus d’articles
                    </button>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>
      <FooterPage />
    </>
  );
}
