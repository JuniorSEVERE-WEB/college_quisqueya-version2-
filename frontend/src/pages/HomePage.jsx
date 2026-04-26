import { useEffect, useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import "./homepage.css";
import API from "../api";
import { motion } from "framer-motion"; // 🔹 Import Framer Motion

export function HomePage() {
  const [slides, setSlides] = useState([]);
  const [current, setCurrent] = useState(0);
  const [welcome, setWelcome] = useState(null);
  const [values, setValues] = useState([]);
  const [articles, setArticles] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // 🔹 États pour l'animation typewriter
  const [titleIndex, setTitleIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [displayedText, setDisplayedText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  // Charger les données
  useEffect(() => {
    async function fetchData() {
      try {
        const [slidesRes, welcomeRes, valuesRes, articlesRes] = await Promise.all([
          API.get("homepage/slides/"),
          API.get("homepage/welcome/"),
          API.get("homepage/values/"),
          API.get("blog/articles/?is_published=true"),
        ]);

        setSlides(slidesRes.data.results || slidesRes.data || []);
        setWelcome(
          welcomeRes.data.results
            ? welcomeRes.data.results[0]
            : Array.isArray(welcomeRes.data)
            ? welcomeRes.data[0]
            : welcomeRes.data
        );
        setValues(valuesRes.data.results || valuesRes.data || []);
        setArticles(articlesRes.data.results || articlesRes.data || []);
        setError("");
      } catch (err) {
        console.error("Erreur chargement homepage:", err);
        setError("Impossible de charger la page d’accueil.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // Animation typewriter
  useEffect(() => {
    if (slides.length === 0) return;
    const titles = slides[current]?.titles || [];
    if (titles.length === 0) return;

    const currentTitle = titles[titleIndex]?.title || "";
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

  // Construire URL images
  const getImageUrl = (img) => {
    if (!img) return "";
    if (/^https?:\/\//i.test(img)) return img;
    const base = API?.defaults?.baseURL || "";
    const root = base.replace(/\/api\/?.*$/, "");
    return `${root}${img.startsWith("/") ? "" : "/"}${img}`;
  };

  const slideInSection = {
    hidden: { opacity: 0, x: -90 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.8, ease: "easeOut" },
    },
  };

  const staggerGroup = {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: 0.14,
        delayChildren: 0.12,
      },
    },
  };

  const slideInCard = {
    hidden: { opacity: 0, x: -55 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.65, ease: "easeOut" },
    },
  };

  return (
    <>
      <HeaderPage />

      {loading && <div className="loading">Chargement…</div>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && (
        <>
          {/* === Section Slides === */}
          {slides.length > 0 && (
            <motion.section
              initial={{ opacity: 0, y: -50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 1 }}
              viewport={{ once: false, amount: 0.3 }}
              className="carroussel"
            >
              <div
                className="carroussel-img"
                style={{
                  backgroundImage: `url(${getImageUrl(slides[current].image)})`,
                }}
              >
                <div className="carroussel-overlay">
                  <h2 className="carroussel-titles">
                    {displayedText}
                    <span className="cursor">|</span>
                  </h2>
                  <p className="carroussel-description">
                    {slides[current].text}
                  </p>
                </div>
              </div>
            </motion.section>
          )}

         {/* === Section Bienvenue === */}
         {welcome && (
          <motion.section
            className="bienvenue-section"
            initial="hidden"
            whileInView="visible"
            variants={slideInSection}
            viewport={{ once: false, amount: 0.25 }}
          >
            <div className="container">
              <div className="bienvenue-card">
                <motion.h1
                  className="bienvenue-title"
                  initial={{ opacity: 0, x: -45 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.75, ease: "easeOut", delay: 0.1 }}
                  viewport={{ once: false, amount: 0.5 }}
                >
                  {welcome.title}
                </motion.h1>
                <motion.p
                  className="bienvenue-text"
                  initial={{ opacity: 0, x: -45 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.75, ease: "easeOut", delay: 0.25 }}
                  viewport={{ once: false, amount: 0.5 }}
                >
                  {welcome.content}
                </motion.p>
              </div>
            </div>
          </motion.section>
        )}

          {/* === Section Valeurs === */}
          {values.length > 0 && (
            <motion.section
              className="valeurs-section"
              initial="hidden"
              whileInView="visible"
              variants={slideInSection}
              viewport={{ once: false, amount: 0.2 }}
            >
              <div className="container">
                <motion.h2
                  className="valeurs-title"
                  initial={{ opacity: 0, x: -55 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.75, ease: "easeOut", delay: 0.1 }}
                  viewport={{ once: false, amount: 0.5 }}
                >
                  Nos Valeurs & Missions
                </motion.h2>
                <motion.div
                  className="valeurs-grid"
                  initial="hidden"
                  whileInView="visible"
                  variants={staggerGroup}
                  viewport={{ once: false, amount: 0.2 }}
                >
                  {values.map((v) => (
                    <motion.div
                      key={v.id}
                      className="valeur-card"
                      variants={slideInCard}
                    >
                      <div className="valeur-icon">{v.icon}</div>
                      <h3>{v.title}</h3>
                      <p>{v.description}</p>
                    </motion.div>
                  ))}
                </motion.div>
              </div>
            </motion.section>
          )}

          {/* === Section Articles === */}
          {articles.length > 0 && (
            <motion.section
              initial="hidden"
              whileInView="visible"
              variants={slideInSection}
              viewport={{ once: false, amount: 0.3 }}
              className="articles-home"
            >
              <div className="container">
                <motion.h2 variants={slideInCard}>Actualités & Articles</motion.h2>

                {/* Grille Desktop */}
                <motion.div
                  className="articles-grid"
                  initial="hidden"
                  whileInView="visible"
                  variants={staggerGroup}
                  viewport={{ once: false, amount: 0.15 }}
                >
                  {articles.slice(0, 4).map((a) => (
                    <motion.div
                      key={a.id}
                      className="article-card"
                      variants={slideInCard}
                    >
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
                    </motion.div>
                  ))}
                </motion.div>

                {/* Carrousel Mobile */}
                <motion.div
                  className="articles-carousel"
                  initial="hidden"
                  whileInView="visible"
                  variants={staggerGroup}
                  viewport={{ once: false, amount: 0.15 }}
                >
                  {articles.slice(0, 4).map((a) => (
                    <motion.div
                      key={a.id}
                      className="article-card"
                      variants={slideInCard}
                    >
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
                    </motion.div>
                  ))}
                </motion.div>
              </div>
            </motion.section>
          )}

          {/* === Bouton Plus d’articles === */}
          <motion.div
      className="more-articles"
      initial={{ opacity: 0, x: -60 }}
      whileInView={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.75, ease: "easeOut", delay: 0.2 }}
      viewport={{ once: false, amount: 0.5 }}
    >
      <a href="/news" className="btn-more">
        Plus d'articles
      </a>
    </motion.div>
            </>
          )}

      <FooterPage />
    </>
  );
}
