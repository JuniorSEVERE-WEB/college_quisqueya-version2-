import { useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import API from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Tente /auth/token/, puis fallback /token/
  const loginRequest = async (username, password) => {
    try {
      return await API.post("auth/token/", { username, password });
    } catch (e) {
      if (e.response?.status === 404) {
        return await API.post("token/", { username, password });
      }
      throw e;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await loginRequest(username, password);
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);

      try {
        const me = await API.get("auth/me/");
        localStorage.setItem("user", JSON.stringify(me.data));
      } catch (_) {}

      if (onLogin) onLogin();
      window.dispatchEvent(new Event("authChanged"));
      navigate("/");
    } catch (err) {
      const detail = err?.response?.data?.detail || "Identifiants invalides";
      setError(detail);
    }
  };

  return (
    <>
      <HeaderPage />
      <div className="login-page" style={{ maxWidth: 420, margin: "24px auto", padding: "0 16px" }}>
        <h2 style={{ textAlign: "center", marginBottom: 16 }}>Connexion</h2>
        <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
          <input
            type="text"
            placeholder="Nom d'utilisateur ou email"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            autoComplete="username"
          />
          <input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
          />
          <button type="submit" style={{ padding: "10px 14px", fontWeight: 600 }}>
            Se connecter
          </button>
        </form>
        {error && <div style={{ color: "red", marginTop: 10 }}>{error}</div>}

        <div style={{ marginTop: 16, textAlign: "center" }}>
          Pas de compte ?{" "}
          <Link to="/register">
            Créer un compte
          </Link>
        </div>
      </div>
      <FooterPage />
    </>
  );
}