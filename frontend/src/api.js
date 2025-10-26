import axios from "axios";

// ✅ Base URL dynamique (locale avec proxy ou production)
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

console.log("API Base URL:", BASE_URL);

const API = axios.create({
  baseURL: BASE_URL ? `${BASE_URL}/api/` : "/api/", // ✅ Utilise le proxy en local
  timeout: 10000,
  withCredentials: false,
  headers: {
    "Content-Type": "application/json",
  },
});

// ---- Ajoute le token à chaque requête si présent ----
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ---- Gestion des réponses et rafraîchissement du token ----
API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Si erreur 401 et pas déjà en train de rafraîchir
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) {
          throw new Error("No refresh token");
        }

        // Essaye de rafraîchir le token
        const response = await axios.post(
          `${BASE_URL || ""}/api/auth/token/refresh/`,
          { refresh: refreshToken }
        );

        const newAccessToken = response.data.access;
        localStorage.setItem("access_token", newAccessToken);

        // Retente la requête originale avec le nouveau token
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return API(originalRequest);

      } catch (refreshError) {
        // Si le rafraîchissement échoue, déconnecter l'utilisateur
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        window.dispatchEvent(new Event("authChanged"));
        
        // Rediriger vers la page de login
        if (window.location.pathname !== "/login") {
          window.location.href = "/login";
        }
        
        return Promise.reject(refreshError);
      }
    }

    // Gestion d'autres erreurs
    if (error.response?.status >= 500) {
      console.error("Server error:", error.response);
    }

    return Promise.reject(error);
  }
);

export default API;
export { BASE_URL };