import axios from "axios";

// 👉 constante qu'on peut réutiliser dans les composants (pour afficher les images)
const BASE_URL = "http://127.0.0.1:8000";

const API = axios.create({
  baseURL: `${BASE_URL}/api/`,
  withCredentials: false,
});

// ---- Ajoute le token à chaque requête si présent ----
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ---- Helper: rafraîchit le token ----
async function refreshAccessToken() {
  const refresh = localStorage.getItem("refresh_token");
  if (!refresh) throw new Error("No refresh token");

  try {
    const { data } = await API.post("auth/token/refresh/", { refresh });
    return data.access;
  } catch (e) {
    if (e.response?.status === 404) {
      const { data } = await API.post("token/refresh/", { refresh });
      return data.access;
    }
    throw e;
  }
}

// ---- Rafraîchissement auto du token sur 401 ----
API.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config || {};
    const status = error.response?.status;

    // évite boucle infinie et double essai
    const isRefreshCall = /(auth\/)?token\/refresh\/$/.test(original.url || "");

    if (status === 401 && !original._retry && !isRefreshCall) {
      original._retry = true;
      try {
        const newAccess = await refreshAccessToken();
        localStorage.setItem("access_token", newAccess);

        original.headers = {
          ...(original.headers || {}),
          Authorization: `Bearer ${newAccess}`,
        };

        window.dispatchEvent(new Event("authChanged"));
        return API(original);
      } catch (e) {
        // échec du refresh: nettoyage et propagation
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        window.dispatchEvent(new Event("authChanged"));
        throw e;
      }
    }

    throw error;
  }
);

export default API;
export { BASE_URL }; // 👉 on exporte aussi BASE_URL pour les images
