// ✅ frontend/src/components/ProtectedPage.jsx
import { Navigate } from "react-router-dom";
import { useEffect, useState } from "react";

export function ProtectedPage({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );
  const [showMessage, setShowMessage] = useState(false);

  useEffect(() => {
    const update = () => setIsLoggedIn(!!localStorage.getItem("access_token"));
    update();
    window.addEventListener("storage", update);
    window.addEventListener("authChanged", update);
    return () => {
      window.removeEventListener("storage", update);
      window.removeEventListener("authChanged", update);
    };
  }, []);

  if (!isLoggedIn) {
    setTimeout(() => setShowMessage(true), 200);

    return (
      <div
        style={{
          textAlign: "center",
          padding: "100px 20px",
          color: "darkred",
          lineHeight: "1.6",
        }}
      >
        <h2>🔒 Accès restreint</h2>
        <p>
          Vous devez être <strong>inscrit comme abonné</strong> pour accéder à ces
          informations.
        </p>
        <p>
          Si vous n’êtes pas un élève ou un professeur de cette école, n’inscrivez
          pas à ces titres.
        </p>
        <p>La direction analysera vos informations avant validation.</p>
        {showMessage && (
          <a
            href="/login"
            style={{
              display: "inline-block",
              marginTop: "20px",
              padding: "10px 20px",
              background: "#001F54",
              color: "white",
              borderRadius: "8px",
              textDecoration: "none",
            }}
          >
            ➜ Se connecter / S’inscrire
          </a>
        )}
      </div>
    );
  }

  return children;
}
