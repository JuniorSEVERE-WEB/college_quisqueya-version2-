// frontend/src/pages/ForgotPassword.jsx
import { useState } from "react";
import axios from "axios";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      // Envoie la requête vers ton backend Django
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
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
        <div className="max-w-md w-full bg-white shadow-md rounded-xl p-8">
          <h2 className="text-2xl font-semibold mb-4 text-center">
            Mot de passe oublié ?
          </h2>
          <p className="text-gray-600 mb-6 text-center">
            Entrez votre adresse email, et nous vous enverrons un lien pour
            réinitialiser votre mot de passe.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Votre adresse email"
              required
              className="w-full border rounded-lg px-4 py-2 focus:ring focus:ring-blue-300"
            />
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Envoyer le lien
            </button>
          </form>

          {message && (
            <p className="text-green-600 text-center mt-4 font-medium">
              {message}
            </p>
          )}
          {error && (
            <p className="text-red-600 text-center mt-4 font-medium">{error}</p>
          )}
        </div>
      </div>
      <FooterPage />
    </>
  );
}
