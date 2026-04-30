import {
  FaGraduationCap,
  FaBook,
  FaBookOpen,
  FaHandshake,
  FaUsers,
  FaTrophy,
  FaGlobe,
  FaHeart,
  FaKey,
  FaDove,
  FaLightbulb,
  FaStar,
  FaSeedling,
  FaSchool,
  FaChalkboardTeacher,
  FaPeace,
  FaAward,
} from "react-icons/fa";
import { GiMicroscope, GiOpenBook, GiStairsGoal } from "react-icons/gi";
import { MdScience } from "react-icons/md";
import "./ValeurIcone.css";

const EMOJI_MAP = {
  "🎓": FaGraduationCap,
  "📚": FaBook,
  "📖": FaBookOpen,
  "🤝": FaHandshake,
  "👥": FaUsers,
  "🏆": FaTrophy,
  "🌍": FaGlobe,
  "🌎": FaGlobe,
  "🌏": FaGlobe,
  "🌱": FaSeedling,
  "🌟": FaStar,
  "⭐": FaStar,
  "💡": FaLightbulb,
  "❤️": FaHeart,
  "🔑": FaKey,
  "🕊️": FaDove,
  "🔬": GiMicroscope,
  "🧪": MdScience,
  "🏫": FaSchool,
  "👨‍🏫": FaChalkboardTeacher,
  "☮️": FaPeace,
  "🎯": GiStairsGoal,
  "🏅": FaAward,
};

// Palette d'accents qui tourne par index — navy/or du collège + variations cohérentes
const ACCENTS = [
  "#1a6fb5",
  "#daa520",
  "#2e7d52",
  "#b5341a",
  "#7b4fa6",
  "#1a9bb5",
];

// Périmètre approximatif du rect arrondi dans le SVG (viewBox 80×80, rect 74×74 rx=14)
const BORDER_PERIMETER = 280;

export function ValeurIcone({ icon, index }) {
  const Icon = EMOJI_MAP[icon];
  const accent = ACCENTS[index % ACCENTS.length];

  return (
    <div className="vi-wrap" style={{ "--vi-accent": accent }}>
      {/* Bordure animée draw-on au survol de la carte */}
      <svg
        className="vi-border"
        viewBox="0 0 80 80"
        fill="none"
        aria-hidden="true"
      >
        <rect
          x="3"
          y="3"
          width="74"
          height="74"
          rx="14"
          stroke={accent}
          strokeWidth="2.5"
          strokeDasharray={BORDER_PERIMETER}
          strokeDashoffset={BORDER_PERIMETER}
        />
      </svg>

      {Icon ? (
        <Icon className="vi-svg" aria-label={icon} />
      ) : (
        // Fallback : l'emoji lui-même, centré dans le même conteneur
        <span className="vi-emoji" aria-label={icon}>
          {icon}
        </span>
      )}
    </div>
  );
}
