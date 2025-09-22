import { useEffect, useState } from "react";
import API from "../api";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchProfile() {
      try {
        // On récupère l'utilisateur connecté
        const userRes = await API.get("users/me/");
        // Selon le rôle, on va chercher le profil associé
        let profileRes = null;
        if (userRes.data.role === "student") {
          profileRes = await API.get(`students/${userRes.data.id}/`);
        } else if (userRes.data.role === "teacher") {
          profileRes = await API.get(`teachers/${userRes.data.id}/`);
        } else if (userRes.data.role === "employee") {
          profileRes = await API.get(`employees/${userRes.data.id}/`);
        }
        setProfile({ ...userRes.data, ...profileRes?.data });
      } catch (e) {
        setError("Erreur lors de la récupération du profil");
      }
    }
    fetchProfile();
  }, []);

  if (error) return <div style={{ color: "red" }}>{error}</div>;
  if (!profile) return <div>Chargement du profil...</div>;

  return (
    <>
      <HeaderPage />
      <div className="profile-page">
        <h2>Mon profil</h2>
        <div>
          <b>Nom d'utilisateur :</b> {profile.username}
        </div>
        <div>
          <b>Rôle :</b> {profile.role}
        </div>
        {/* Affiche d'autres infos selon le profil */}
      </div>
      <FooterPage />
    </>
  );
}
