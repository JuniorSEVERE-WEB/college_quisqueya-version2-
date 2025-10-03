import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import API from "../api";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import "./articledetail.css";

export default function ArticleDetailPage() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);

  const [comments, setComments] = useState([]);
  const [nextUrl, setNextUrl] = useState(null);

  const [newComment, setNewComment] = useState("");
  const [replyingTo, setReplyingTo] = useState(null);

  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState("");

  const getImageUrl = (img) => {
    if (!img) return "";
    if (/^https?:\/\//i.test(img)) return img;
    const base = API?.defaults?.baseURL || "";
    const root = base.replace(/\/api\/?.*$/, "");
    return `${root}${img.startsWith("/") ? "" : "/"}${img}`;
  };

  // --- Charger l’article ---
  useEffect(() => {
    async function fetchArticle() {
      try {
        const res = await API.get(`blog/articles/${id}/`);
        setArticle(res.data);
        setError("");
      } catch (e) {
        setError("Impossible de charger cet article.");
      } finally {
        setLoading(false);
      }
    }
    fetchArticle();
  }, [id]);

  // --- Charger les commentaires (page 1) ---
  useEffect(() => {
    async function fetchComments() {
      try {
        const res = await API.get("blog/comments/", {
          params: { article: id, page: 1, page_size: 10 },
        });
        setComments(res.data.results || []);
        setNextUrl(res.data.next || null);
      } catch (e) {
        console.error("Erreur chargement commentaires", e);
      }
    }
    if (id) fetchComments();
  }, [id]);

  // --- Charger plus de commentaires ---
  async function loadMore() {
    if (!nextUrl) return;
    setLoadingMore(true);
    try {
      const res = await API.get(
        nextUrl.replace(/^https?:\/\/[^/]+\/api\//, "")
      );
      setComments((prev) => [...prev, ...(res.data.results || [])]);
      setNextUrl(res.data.next || null);
    } catch (e) {
      console.error("Erreur lors du chargement des commentaires suivants", e);
    } finally {
      setLoadingMore(false);
    }
  }

  // --- Poster un commentaire (ou une réponse) ---
  const postComment = async (parentId = null) => {
    if (!newComment.trim()) return;
    try {
      const res = await API.post("blog/comments/", {
        article: id,
        text: newComment,
        parent: parentId,
      });
      setComments((prev) => [res.data, ...prev]);
      setNewComment("");
      setReplyingTo(null);
    } catch (e) {
      alert("Erreur lors de l'ajout du commentaire (êtes-vous connecté ?)");
    }
  };

  // --- Réactions article ---
  const reactToArticle = async (reactionType) => {
    try {
      await API.post("blog/reactions/", {
        article: id,
        reaction_type: reactionType,
      });
      const res = await API.get(`blog/articles/${id}/`);
      setArticle(res.data);
    } catch (e) {
      alert("Erreur lors de la réaction.");
    }
  };

  // --- Réactions commentaire ---
  const reactToComment = async (commentId, reactionType) => {
    try {
      await API.post("blog/reactions/", {
        comment: commentId,
        reaction_type: reactionType,
      });
      const res = await API.get("blog/comments/", {
        params: { article: id, page: 1, page_size: comments.length },
      });
      setComments(res.data.results || res.data);
    } catch (e) {
      alert("Erreur lors de la réaction au commentaire.");
    }
  };

  // --- Affichage récursif des commentaires ---
  const renderComments = (commentList, parentId = null) => {
    return commentList
      .filter((c) => (parentId ? c.parent === parentId : !c.parent))
      .map((c) => (
        <div
          key={c.id}
          className={`comment ${c.parent ? "reply" : "root"}`}
        >
          <div className="comment-meta">
            <strong>{c.user || "Utilisateur"}</strong> ·{" "}
            {new Date(c.date_posted).toLocaleDateString("fr-FR")}
          </div>
          <div className="comment-text">{c.text}</div>

          {/* Réactions */}
          <div className="comment-reactions">
            <button onClick={() => reactToComment(c.id, "like")}>
              👍 {c.likes_count || 0}
            </button>
            <button onClick={() => reactToComment(c.id, "dislike")}>
              👎 {c.dislikes_count || 0}
            </button>
            <button onClick={() => setReplyingTo(c.id)}>Répondre</button>
          </div>

          {/* Formulaire de réponse */}
          {replyingTo === c.id && (
            <div className="reply-form">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Votre réponse..."
              />
              <button onClick={() => postComment(c.id)}>Envoyer</button>
              <button onClick={() => setReplyingTo(null)}>Annuler</button>
            </div>
          )}

          {/* Réponses récursives */}
          <div className="replies">{renderComments(commentList, c.id)}</div>
        </div>
      ));
  };

  return (
    <>
      <HeaderPage />

      <div className="article-detail">
        {loading && <div>Chargement…</div>}
        {!loading && error && <div>{error}</div>}

        {!loading && article && (
          <div className="article-container">
            <h1 className="article-title">{article.title}</h1>
            <div className="article-meta">
              Posté le{" "}
              {new Date(article.date_published).toLocaleDateString("fr-FR")} par{" "}
              {article.author?.username || "Admin"}
            </div>
            <img
              src={getImageUrl(article.image)}
              alt={article.title}
              className="article-image"
            />
            <p className="article-desc">{article.description}</p>

            {/* Réactions article */}
            <div className="article-reactions">
              <button onClick={() => reactToArticle("like")}>
                👍 {article.likes_count}
              </button>
              <button onClick={() => reactToArticle("dislike")}>
                👎 {article.dislikes_count}
              </button>
            </div>

            {/* Commentaires */}
            <div className="comments-section">
              <h3>Commentaires</h3>

              {/* Formulaire principal */}
              <div className="comment-form">
                <textarea
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Écrire un commentaire..."
                />
                <button onClick={() => postComment(null)}>Publier</button>
              </div>

              {comments.length === 0 ? (
                <p>Aucun commentaire pour le moment.</p>
              ) : (
                renderComments(comments)
              )}

              {/* Bouton Voir plus */}
              {nextUrl && (
                <div className="load-more">
                  <button
                    onClick={loadMore}
                    disabled={loadingMore}
                    className="btn-load-more"
                  >
                    {loadingMore ? "Chargement…" : "Voir plus de commentaires"}
                  </button>
                </div>
              )}
            </div>

            <div className="back-link">
              <Link to="/news">← Retour aux actualités</Link>
            </div>
          </div>
        )}
      </div>

      <FooterPage />
    </>
  );
}
