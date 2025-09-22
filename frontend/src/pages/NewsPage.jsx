import { useEffect, useState } from "react";
import API from "../api";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";

export default function NewsPage() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    API.get("articles/")
      .then((res) => setArticles(res.data))
      .catch(() => setArticles([]));
  }, []);

  return (
    <>
    <HeaderPage />
      <div className="news-page">
        <h2>Newsddd</h2>
        {articles.length === 0 && <div>No news at the moment.</div>}
        {articles.map((article) => (
          <div key={article.id} className="article-card">
            <h3>{article.title}</h3>
            <div style={{ fontSize: "0.9em", color: "#888" }}>
              by {article.author} |{" "}
              {new Date(article.published_at).toLocaleDateString()}
            </div>
            <p>
              {article.content.slice(0, 200)}
              {article.content.length > 200 ? "..." : ""}
            </p>
          </div>
        ))}      

      </div>
      <FooterPage />
    </>
  );
}
