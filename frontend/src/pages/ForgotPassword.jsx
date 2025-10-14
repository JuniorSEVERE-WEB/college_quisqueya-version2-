// frontend/src/pages/ForgotPassword.jsx
import { useState } from "react";
import axios from "axios";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import "./forgotpassword.css";  // 👈 import du style

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      await axios.post("http://127.0.0.1:8000/api/auth/password-reset/", { email });
      setMessage("📬 Un lien de réinitialisation vous a été envoyé par email.");
      setEmail("");
    } catch (err) {
      setError("❌ Une erreur est survenue. Vérifiez l'adresse email.");
    }
  };

  return (
    <>
      <HeaderPage />

      <div className="forgot-container">
        <div className="forgot-card">
          <h2>Mot de passe oublié ?</h2>
          <p>
            Entrez votre adresse email, et nous vous enverrons un lien pour
            réinitialiser votre mot de passe.
          </p>

          <form onSubmit={handleSubmit}>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Votre adresse email"
              required
            />
            <button type="submit">Envoyer le lien</button>
          </form>

          {message && (
            <p className="forgot-message success">{message}</p>
          )}
          {error && (
            <p className="forgot-message error">{error}</p>
          )}
        </div>
      </div>

      <FooterPage />
    </>
  );
}
