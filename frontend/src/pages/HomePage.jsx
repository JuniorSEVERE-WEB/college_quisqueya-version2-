import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import "./homepage.css";
import API from "../api";
import { motion, AnimatePresence } from "framer-motion";
import { getMediaUrl } from "../utils/media";
import { ValeurIcone } from "../components/ValeurIcone";
import {
  FaGraduationCap,
  FaUsers,
  FaTrophy,
  FaSchool,
  FaChevronLeft,
  FaChevronRight,
  FaArrowRight,
  FaCalendarAlt,
} from "react-icons/fa";

const STATS = [
  { value: "1985", suffix: "",   label: "Année de Fondation" },
  { value: "40",   suffix: "+",  label: "Années d'Excellence" },
  { value: "600",  suffix: "+",  label: "Élèves par Année" },
  { value: "100",  suffix: "%",  label: "Engagement Pédagogique" },
];

const STAT_ICONS = [FaSchool, FaTrophy, FaUsers, FaGraduationCap];

const fadeUp = {
  hidden:  { opacity: 0, y: 28 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } },
};

const stagger = {
  hidden:   {},
  visible:  { transition: { staggerChildren: 0.12, delayChildren: 0.1 } },
};

export function HomePage() {
  const [slides,   setSlides]   = useState([]);
  const [current,  setCurrent]  = useState(0);
  const [welcome,  setWelcome]  = useState(null);
  const [values,   setValues]   = useState([]);
  const [articles, setArticles] = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState("");

  // Typewriter state
  const [titleIndex,     setTitleIndex]     = useState(0);
  const [charIndex,      setCharIndex]      = useState(0);
  const [displayedText,  setDisplayedText]  = useState("");
  const [isDeleting,     setIsDeleting]     = useState(false);

  // ── Fetch data ────────────────────────────────────────────────────────────
  useEffect(() => {
    async function fetchData() {
      try {
        const [slidesRes, welcomeRes, valuesRes, articlesRes] = await Promise.all([
          API.get("homepage/slides/"),
          API.get("homepage/welcome/"),
          API.get("homepage/values/"),
          API.get("blog/articles/?is_published=true"),
        ]);
        setSlides(slidesRes.data.results   || slidesRes.data   || []);
        setWelcome(
          welcomeRes.data.results
            ? welcomeRes.data.results[0]
            : Array.isArray(welcomeRes.data)
            ? welcomeRes.data[0]
            : welcomeRes.data
        );
        setValues(valuesRes.data.results     || valuesRes.data     || []);
        setArticles(articlesRes.data.results || articlesRes.data   || []);
      } catch (err) {
        console.error("Erreur chargement homepage:", err);
        setError("Impossible de charger la page d'accueil.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  // ── Auto-advance carousel ─────────────────────────────────────────────────
  useEffect(() => {
    if (slides.length <= 1) return;
    const t = setInterval(() => setCurrent((p) => (p + 1) % slides.length), 6000);
    return () => clearInterval(t);
  }, [slides.length]);

  // ── Reset typewriter when slide changes ───────────────────────────────────
  useEffect(() => {
    setCharIndex(0);
    setTitleIndex(0);
    setDisplayedText("");
    setIsDeleting(false);
  }, [current]);

  // ── Typewriter animation ──────────────────────────────────────────────────
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
      timeout = setTimeout(() => setIsDeleting(true), 1800);
    } else if (isDeleting && charIndex > 0) {
      timeout = setTimeout(() => {
        setDisplayedText(currentTitle.substring(0, charIndex - 1));
        setCharIndex(charIndex - 1);
      }, 60);
    } else if (isDeleting && charIndex === 0) {
      setIsDeleting(false);
      setTitleIndex((prev) => (prev + 1) % titles.length);
    }
    return () => clearTimeout(timeout);
  }, [charIndex, isDeleting, titleIndex, slides, current]);

  const prevSlide = () => setCurrent((p) => (p - 1 + slides.length) % slides.length);
  const nextSlide = () => setCurrent((p) => (p + 1) % slides.length);

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <>
      <HeaderPage />

      {/* Loading */}
      {loading && (
        <div className="flex items-center justify-center min-h-screen bg-light-bg">
          <div className="flex flex-col items-center gap-4">
            <div className="w-12 h-12 border-4 border-navy border-t-gold rounded-full animate-spin" />
            <p className="text-navy font-semibold tracking-wide">Chargement…</p>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex items-center justify-center min-h-screen bg-light-bg px-4">
          <div className="flex flex-col items-center gap-5 text-center max-w-sm">
            <div className="w-16 h-16 rounded-full bg-navy/8 flex items-center justify-center">
              <svg className="w-8 h-8 text-navy/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
              </svg>
            </div>
            <div>
              <p className="text-navy font-bold text-lg mb-1">Connexion impossible</p>
              <p className="text-sm text-[#666] leading-relaxed">
                Vérifiez votre connexion internet et réessayez.
              </p>
            </div>
            <button
              onClick={() => { setError(""); setLoading(true); window.location.reload(); }}
              className="px-6 py-2.5 bg-navy text-white text-sm font-semibold rounded-full hover:bg-navy/80 transition-colors duration-200"
            >
              Réessayer
            </button>
          </div>
        </div>
      )}

      {!loading && !error && (
        <>
          {/* ══════════════════════════════════════════════════════════════════
              HERO — Carousel plein écran
          ══════════════════════════════════════════════════════════════════ */}
          {slides.length > 0 && (
            <section className="relative h-[85vh] min-h-[520px] overflow-hidden">

              {/* Background image with crossfade */}
              <AnimatePresence mode="wait">
                <motion.div
                  key={current}
                  initial={{ opacity: 0, scale: 1.06 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.9 }}
                  className="absolute inset-0 bg-cover bg-top"
                  style={{ backgroundImage: `url(${getMediaUrl(slides[current].image)})` }}
                />
              </AnimatePresence>

              {/* Gradient overlay */}
              <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-black/45 to-black/80 z-10" />

              {/* Content */}
              <div className="relative z-20 flex flex-col items-center justify-end sm:justify-center h-full text-white text-center px-4 pb-16 sm:pb-0">
                <motion.div
                  key={`content-${current}`}
                  initial={{ opacity: 0, y: 32 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.7, delay: 0.25 }}
                  className="max-w-4xl mx-auto space-y-5"
                >
                  {/* Badge fondation */}
                  <span className="inline-block px-4 py-1.5 bg-gold/20 border border-gold/50 text-gold-light text-xs font-bold rounded-full backdrop-blur-sm tracking-widest uppercase">
                    Fondé en 1985 · Léogâne, Haïti
                  </span>

                  {/* Typewriter title */}
                  <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black tracking-tight leading-none text-white drop-shadow-2xl min-h-[1.2em]">
                    {displayedText || " "}
                    <span className="tw-cursor text-gold">|</span>
                  </h1>

                  {/* Description slide */}
                  <p className="text-sm sm:text-base md:text-lg text-white/80 max-w-2xl mx-auto leading-relaxed">
                    {slides[current].text}
                  </p>

                  {/* CTA buttons */}
                  <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
                    <Link
                      to="/register"
                      className="inline-flex items-center justify-center gap-2 px-8 py-3.5 bg-gold hover:bg-gold-light text-navy font-bold rounded-full transition-all duration-300 hover:shadow-xl hover:shadow-gold/30 hover:-translate-y-0.5"
                    >
                      S'inscrire maintenant
                      <FaArrowRight size={13} />
                    </Link>
                    <Link
                      to="/contact"
                      className="inline-flex items-center justify-center gap-2 px-8 py-3.5 bg-white/10 border border-white/30 text-white font-semibold rounded-full backdrop-blur-sm hover:bg-white/20 transition-all duration-300"
                    >
                      Nous contacter
                    </Link>
                  </div>
                </motion.div>
              </div>

              {/* Navigation arrows */}
              {slides.length > 1 && (
                <>
                  <button
                    onClick={prevSlide}
                    aria-label="Slide précédent"
                    className="absolute left-3 md:left-8 top-1/2 -translate-y-1/2 z-30 w-11 h-11 bg-black/40 hover:bg-black/70 text-white rounded-full flex items-center justify-center transition-all duration-200 hover:scale-110"
                  >
                    <FaChevronLeft size={14} />
                  </button>
                  <button
                    onClick={nextSlide}
                    aria-label="Slide suivant"
                    className="absolute right-3 md:right-8 top-1/2 -translate-y-1/2 z-30 w-11 h-11 bg-black/40 hover:bg-black/70 text-white rounded-full flex items-center justify-center transition-all duration-200 hover:scale-110"
                  >
                    <FaChevronRight size={14} />
                  </button>
                </>
              )}

              {/* Dot indicators */}
              {slides.length > 1 && (
                <div className="absolute bottom-7 left-1/2 -translate-x-1/2 z-30 flex gap-2">
                  {slides.map((_, i) => (
                    <button
                      key={i}
                      onClick={() => setCurrent(i)}
                      aria-label={`Slide ${i + 1}`}
                      className={`h-2 rounded-full transition-all duration-300 ${
                        i === current
                          ? "w-7 bg-gold"
                          : "w-2 bg-white/50 hover:bg-white/80"
                      }`}
                    />
                  ))}
                </div>
              )}
            </section>
          )}

          {/* ══════════════════════════════════════════════════════════════════
              STATS BAR
          ══════════════════════════════════════════════════════════════════ */}
          <motion.section
            className="bg-navy py-10"
            initial="hidden"
            whileInView="visible"
            variants={stagger}
            viewport={{ once: false, amount: 0.3 }}
          >
            <div className="max-w-5xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-6">
              {STATS.map((stat, i) => {
                const Icon = STAT_ICONS[i];
                return (
                  <motion.div key={i} variants={fadeUp} className="text-center group">
                    <div className="flex justify-center mb-2">
                      <Icon className="text-gold/60 group-hover:text-gold transition-colors duration-300" size={22} />
                    </div>
                    <p className="text-3xl md:text-4xl font-black text-gold leading-none">
                      {stat.value}<span className="text-xl">{stat.suffix}</span>
                    </p>
                    <p className="text-white/55 text-xs mt-1.5 tracking-wide">{stat.label}</p>
                  </motion.div>
                );
              })}
            </div>
          </motion.section>

          {/* ══════════════════════════════════════════════════════════════════
              BIENVENUE
          ══════════════════════════════════════════════════════════════════ */}
          {welcome && (
            <motion.section
              className="py-16 md:py-24 bg-white"
              initial="hidden"
              whileInView="visible"
              variants={stagger}
              viewport={{ once: false, amount: 0.2 }}
            >
              <div className="max-w-4xl mx-auto px-4">
                <motion.div
                  variants={fadeUp}
                  className="relative bg-white rounded-2xl border border-navy/10 shadow-xl p-8 md:p-12 overflow-hidden"
                >
                  {/* Accent bar haut */}
                  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-navy via-gold to-navy" />

                  <motion.h2
                    variants={fadeUp}
                    className="text-2xl md:text-3xl font-black text-navy-mid mb-3 text-center"
                  >
                    {welcome.title}
                  </motion.h2>
                  <div className="w-16 h-1 bg-gradient-to-r from-navy to-gold mx-auto mb-7 rounded-full" />

                  <motion.p
                    variants={fadeUp}
                    className="text-[#2b2b2b] text-base md:text-lg leading-relaxed text-justify bienvenue-dropcap"
                  >
                    {welcome.content}
                  </motion.p>
                </motion.div>
              </div>
            </motion.section>
          )}

          {/* ══════════════════════════════════════════════════════════════════
              NOS VALEURS & MISSIONS
          ══════════════════════════════════════════════════════════════════ */}
          {values.length > 0 && (
            <motion.section
              className="py-16 md:py-24 bg-light-bg"
              initial="hidden"
              whileInView="visible"
              variants={stagger}
              viewport={{ once: false, amount: 0.15 }}
            >
              <div className="max-w-6xl mx-auto px-4">
                {/* Section header */}
                <motion.div variants={fadeUp} className="text-center mb-12">
                  <span className="inline-block px-3 py-1 bg-navy/6 text-navy text-xs font-bold uppercase tracking-widest rounded-full mb-3">
                    Notre ADN
                  </span>
                  <h2 className="text-3xl md:text-4xl font-black text-navy-mid">
                    Nos Valeurs & Missions
                  </h2>
                  <div className="w-16 h-1 bg-gradient-to-r from-navy to-gold mx-auto mt-4 rounded-full" />
                </motion.div>

                {/* Cards grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                  {values.map((v, index) => (
                    <motion.div
                      key={v.id}
                      variants={fadeUp}
                      className="group bg-white rounded-2xl p-7 shadow-sm border border-transparent hover:border-navy/10 hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
                    >
                      <div className="mb-4">
                        <ValeurIcone icon={v.icon} index={index} />
                      </div>
                      <h3 className="text-base font-bold text-navy-mid mb-2">{v.title}</h3>
                      <p className="text-[#555] text-sm leading-relaxed">{v.description}</p>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.section>
          )}

          {/* ══════════════════════════════════════════════════════════════════
              ACTUALITÉS & ARTICLES
          ══════════════════════════════════════════════════════════════════ */}
          {articles.length > 0 && (
            <motion.section
              className="py-16 md:py-24 bg-white"
              initial="hidden"
              whileInView="visible"
              variants={stagger}
              viewport={{ once: false, amount: 0.1 }}
            >
              <div className="max-w-6xl mx-auto px-4">
                {/* Section header */}
                <motion.div variants={fadeUp} className="text-center mb-12">
                  <span className="inline-block px-3 py-1 bg-navy/6 text-navy text-xs font-bold uppercase tracking-widest rounded-full mb-3">
                    Restez informés
                  </span>
                  <h2 className="text-3xl md:text-4xl font-black text-navy-mid">
                    Actualités & Articles
                  </h2>
                  <div className="w-16 h-1 bg-gradient-to-r from-navy to-gold mx-auto mt-4 rounded-full" />
                </motion.div>

                {/* Desktop grid — 2 col sur tablette, 4 col sur large */}
                <div className="hidden md:grid grid-cols-2 lg:grid-cols-4 gap-5">
                  {articles.slice(0, 4).map((a) => (
                    <motion.article
                      key={a.id}
                      variants={fadeUp}
                      className="group flex flex-col bg-white rounded-2xl overflow-hidden shadow-sm border border-navy/5 hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
                    >
                      {/* Image */}
                      <div className="aspect-video overflow-hidden">
                        <div
                          className="w-full h-full bg-cover bg-center group-hover:scale-105 transition-transform duration-500"
                          style={{ backgroundImage: `url(${getMediaUrl(a.image)})` }}
                        />
                      </div>

                      {/* Body */}
                      <div className="flex flex-col flex-1 p-5 gap-2.5">
                        <div className="flex items-center gap-1.5 text-[11px] text-[#556] font-medium">
                          <FaCalendarAlt size={9} className="text-gold" />
                          {new Date(a.date_published).toLocaleDateString("fr-FR")}
                        </div>
                        <h3 className="text-sm font-bold text-navy leading-snug line-clamp-2">
                          {a.title}
                        </h3>
                        <p className="text-xs text-[#555] leading-relaxed flex-1 line-clamp-3">
                          {a.description}
                        </p>
                        <Link
                          to={`/news/${a.id}`}
                          className="inline-flex items-center gap-1.5 text-xs font-semibold text-navy hover:text-gold transition-colors duration-200 group/lnk mt-1"
                        >
                          Lire plus
                          <FaArrowRight size={9} className="group-hover/lnk:translate-x-1 transition-transform" />
                        </Link>
                      </div>
                    </motion.article>
                  ))}
                </div>

                {/* Mobile horizontal carousel */}
                <div className="md:hidden flex overflow-x-auto gap-4 pb-3 snap-x snap-mandatory scroll-smooth -mx-4 px-4">
                  {articles.slice(0, 4).map((a) => (
                    <article
                      key={a.id}
                      className="flex-none w-[78vw] max-w-[300px] snap-center flex flex-col bg-white rounded-2xl overflow-hidden shadow-md border border-navy/5"
                    >
                      <div
                        className="aspect-video bg-cover bg-center"
                        style={{ backgroundImage: `url(${getMediaUrl(a.image)})` }}
                      />
                      <div className="flex flex-col flex-1 p-4 gap-2">
                        <div className="flex items-center gap-1.5 text-[11px] text-[#556]">
                          <FaCalendarAlt size={9} className="text-gold" />
                          {new Date(a.date_published).toLocaleDateString("fr-FR")}
                        </div>
                        <h3 className="text-sm font-bold text-navy leading-snug line-clamp-2">
                          {a.title}
                        </h3>
                        <p className="text-xs text-[#555] line-clamp-3">{a.description}</p>
                        <Link
                          to={`/news/${a.id}`}
                          className="inline-flex items-center gap-1 text-xs font-semibold text-navy hover:text-gold transition-colors mt-1"
                        >
                          Lire plus <FaArrowRight size={9} />
                        </Link>
                      </div>
                    </article>
                  ))}
                </div>

                {/* CTA voir tout */}
                <motion.div variants={fadeUp} className="text-center mt-10">
                  <Link
                    to="/news"
                    className="inline-flex items-center gap-2 px-8 py-3.5 bg-navy text-white font-semibold rounded-full hover:bg-navy-mid hover:shadow-lg transition-all duration-300 hover:-translate-y-0.5"
                  >
                    Voir toutes les actualités
                    <FaArrowRight size={13} />
                  </Link>
                </motion.div>
              </div>
            </motion.section>
          )}

          {/* ══════════════════════════════════════════════════════════════════
              CTA BANNER — Inscription
          ══════════════════════════════════════════════════════════════════ */}
          <motion.section
            className="relative py-20 bg-navy overflow-hidden"
            initial="hidden"
            whileInView="visible"
            variants={stagger}
            viewport={{ once: false, amount: 0.3 }}
          >
            {/* Decorative blobs */}
            <div className="absolute -top-20 -right-20 w-72 h-72 bg-gold/5 rounded-full pointer-events-none" />
            <div className="absolute -bottom-20 -left-20 w-96 h-96 bg-gold/5 rounded-full pointer-events-none" />

            <div className="relative z-10 max-w-3xl mx-auto px-4 text-center">
              <motion.span
                variants={fadeUp}
                className="inline-block px-3 py-1 bg-gold/20 text-gold-light text-xs font-bold uppercase tracking-widest rounded-full mb-5"
              >
                Rejoignez notre communauté
              </motion.span>

              <motion.h2
                variants={fadeUp}
                className="text-3xl md:text-4xl font-black text-white mb-4 leading-tight"
              >
                Bâtissez votre avenir au<br />
                <span className="text-gold">Collège Quisqueya</span>
              </motion.h2>

              <motion.p
                variants={fadeUp}
                className="text-white/65 mb-9 text-base md:text-lg leading-relaxed max-w-xl mx-auto"
              >
                Depuis 1985, nous formons les leaders de demain avec excellence,
                rigueur et bienveillance au cœur de Léogâne.
              </motion.p>

              <motion.div
                variants={fadeUp}
                className="flex flex-col sm:flex-row gap-3 justify-center"
              >
                <Link
                  to="/register"
                  className="inline-flex items-center justify-center gap-2 px-8 py-3.5 bg-gold text-navy font-bold rounded-full hover:bg-gold-light transition-all duration-300 hover:shadow-xl hover:shadow-gold/30 hover:-translate-y-0.5"
                >
                  S'inscrire maintenant
                  <FaArrowRight size={13} />
                </Link>
                <Link
                  to="/about"
                  className="inline-flex items-center justify-center gap-2 px-8 py-3.5 border border-white/25 text-white font-semibold rounded-full hover:bg-white/10 transition-all duration-300"
                >
                  En savoir plus
                </Link>
              </motion.div>
            </div>
          </motion.section>
        </>
      )}

      <FooterPage />
    </>
  );
}
