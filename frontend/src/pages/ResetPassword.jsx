// frontend/src/pages/ResetPassword.jsx
import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";

export default function ResetPassword() {
  const { uidb64, token } = useParams();
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    if (password1 !== password2) {
      setError("Les mots de passe ne correspondent pas.");
      return;
    }

    try {
      await axios.post(
        `http://127.0.0.1:8000/reset/${uidb64}/${token}/`,
        {
          new_password1: password1,
          new_password2: password2,
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      setMessage("✅ Mot de passe réinitialisé avec succès !");
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      setError("❌ Le lien est invalide ou a expiré.");
    }
  };

  return (
    <>
      <HeaderPage />
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
        <div className="max-w-md w-full bg-white shadow-md rounded-xl p-8">
          <h2 className="text-2xl font-semibold mb-4 text-center">
            Réinitialiser votre mot de passe
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="password"
              value={password1}
              onChange={(e) => setPassword1(e.target.value)}
              placeholder="Nouveau mot de passe"
              required
              className="w-full border rounded-lg px-4 py-2 focus:ring focus:ring-blue-300"
            />
            <input
              type="password"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              placeholder="Confirmer le mot de passe"
              required
              className="w-full border rounded-lg px-4 py-2 focus:ring focus:ring-blue-300"
            />
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Réinitialiser
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
