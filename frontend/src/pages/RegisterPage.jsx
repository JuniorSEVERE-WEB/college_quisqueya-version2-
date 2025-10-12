// frontend/src/pages/RegisterPage.jsx
import { useEffect, useRef, useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import API from "../api";
import "./registerpage.css"; // 👈 style des inputs + boutons + cartes

// Titres lisibles par rôle
const ROLE_TITLES = {
  abonne: "Abonné(e)",
  student: "Étudiant(e)",
  professor: "Professeur(e)",
  alumni: "Ancien/Ancienne",
};

export default function RegisterPage() {
  const [role, setRole] = useState("");
  const [classes, setClasses] = useState([]);
  const [programs, setPrograms] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [loadingClasses, setLoadingClasses] = useState(false);
  const [loadingPrograms, setLoadingPrograms] = useState(false);
  const [loadingSubjects, setLoadingSubjects] = useState(false);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");
  const formRef = useRef(null);
  const [formKey, setFormKey] = useState(0); // force remount pour reset total

  useEffect(() => {
    setMsg("");
    setErr("");
  }, [role]);

  // ⏱️ Efface automatiquement le message de succès après 5 secondes
  useEffect(() => {
    if (msg) {
      const timer = setTimeout(() => setMsg(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [msg]);

  // ⏱️ Efface automatiquement le message d’erreur après 5 secondes
  useEffect(() => {
    if (err) {
      const timer = setTimeout(() => setErr(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [err]);

  // Charger les classes (programs d'abord, puis fallback academics)
  // ✅ Charger les classes (endpoint corrigé et logique nettoyée)
   // ✅ Charger les classes pour les étudiants depuis la même source que le backend
useEffect(() => {
  if (role === "student") {
    setLoadingClasses(true);
    setClasses([]);
    setErr("");

    // on va chercher les classes via l'endpoint utilisé aussi par l’inscription backend
    API.get("academics/classrooms/active/")
      .then((res) => {
        const data = Array.isArray(res.data)
          ? res.data
          : res.data?.results || [];
        console.log("🎓 Classes chargées :", data);
        setClasses(data);
      })
      .catch((error) => {
        console.error("Erreur lors du chargement des classes :", error);
        setErr("Impossible de charger les classes. Veuillez réessayer.");
      })
      .finally(() => setLoadingClasses(false));
  } else {
    setClasses([]);
  }
}, [role]);



  // Charger programmes et matières pour Professeur
  useEffect(() => {
    if (role === "professor") {
      setLoadingPrograms(true);
      setLoadingSubjects(true);
      setPrograms([]);
      setSubjects([]);

      API.get("programs/public/")
        .then((res) =>
          setPrograms(Array.isArray(res.data) ? res.data : res.data?.results || [])
        )
        .catch(() => setErr("Impossible de charger les programmes."))
        .finally(() => setLoadingPrograms(false));

      API.get("subjects/public/")
        .then((res) =>
          setSubjects(Array.isArray(res.data) ? res.data : res.data?.results || [])
        )
        .catch(() => setErr("Impossible de charger les matières."))
        .finally(() => setLoadingSubjects(false));
    }
  }, [role]);

  const hardResetForm = () => {
    try {
      formRef.current?.reset();
    } catch {}
    setFormKey((k) => k + 1); // remonte le form pour reset defaultValue/select/file inputs
  };

  const handleChangeRole = () => {
    hardResetForm();
    setRole("");
    setMsg("");
    setErr("");
    setClasses([]);
    setPrograms([]);
    setSubjects([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");
    setErr("");
    const form = new FormData(e.currentTarget);

    try {
      if (role === "abonne") {
        await API.post("auth/register/abonne/", {
          username: form.get("username"),
          email: form.get("email"),
          password1: form.get("password1"),
          password2: form.get("password2"),
        });
        setMsg("Compte créé. Vous pouvez vous connecter.");
      } else if (role === "student") {
        const fd = new FormData();
        [
          "username",
          "email",
          "password1",
          "password2",
          "first_name",
          "last_name",
          "date_of_birth",
          "parent_phone",
          "student_phone",
          "parent_email",
          "classroom",
        ].forEach((k) => {
          if (form.get(k)) fd.append(k, form.get(k));
        });
        if (form.get("birth_certificate"))
          fd.append("birth_certificate", form.get("birth_certificate"));
        if (form.get("last_school_report"))
          fd.append("last_school_report", form.get("last_school_report"));

        await API.post("students/register/", fd, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setMsg("Demande envoyée. En attente de validation de l’administration.");
      } else if (role === "professor") {
        const fd = new FormData();
        [
          "username",
          "email",
          "password1",
          "password2",
          "first_name",
          "last_name",
          "department",
          "hire_date",
          "program",
        ].forEach((k) => {
          if (form.get(k)) fd.append(k, form.get(k));
        });
        for (let s of form.getAll("subjects")) {
          fd.append("subjects", s);
        }

        await API.post("professors/register/", fd);
        setMsg("Demande envoyée. En attente de validation de l’administration.");
      } else if (role === "alumni") {
        const fd = new FormData();
        [
          "username",
          "email",
          "password1",
          "password2",
          "first_name",
          "last_name",
          "year_left",
          "promo_name",
          "years_interval",
        ].forEach((k) => {
          if (form.get(k)) fd.append(k, form.get(k));
        });
        if (form.get("proof_document"))
          fd.append("proof_document", form.get("proof_document"));

        await API.post("alumni/register/", fd, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        setMsg("Demande envoyée. En attente de validation de l’administration.");
      }
    } catch (e2) {
      const detail = e2?.response?.data || e2?.message || "Erreur d’inscription.";
      setErr(typeof detail === "string" ? detail : JSON.stringify(detail));
    } finally {
      hardResetForm();
    }
  };

  return (
    <>
      <HeaderPage />
      <div style={{ maxWidth: 900, margin: "24px auto", padding: "0 16px" }}>
        <h2 style={{ textAlign: "center", marginBottom: 16 }}>S'inscrire comme :</h2>

        {!role && (
          <div className="role-selection">
            <div className="role-card" onClick={() => setRole("abonne")}>
              <div className="icon">🌐</div>
              Abonné(e)
            </div>
            <div className="role-card" onClick={() => setRole("student")}>
              <div className="icon">🎓</div>
              Étudiant(e)
            </div>
            <div className="role-card" onClick={() => setRole("professor")}>
              <div className="icon">📘</div>
              Professeur(e)
            </div>
            <div className="role-card" onClick={() => setRole("alumni")}>
              <div className="icon">🏅</div>
              Ancien/Ancienne
            </div>
          </div>
        )}

        {role && (
          <form
            key={formKey}
            ref={formRef}
            onSubmit={handleSubmit}
            className="form-section"
          >
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <h3 style={{ margin: 0 }}>{ROLE_TITLES[role] || "Inscription"}</h3>
              <button
                type="button"
                onClick={handleChangeRole}
                className="form-button"
                style={{ marginLeft: "auto" }}
              >
                Changer
              </button>
            </div>

            {/* Champs communs */}
            <input
              className="form-input"
              name="username"
              placeholder="Nom d'utilisateur"
              required
              autoComplete="off"
            />
            <input
              className="form-input"
              name="email"
              type="email"
              placeholder="Email"
              required
              autoComplete="off"
            />
            <input
              className="form-input"
              name="password1"
              type="password"
              placeholder="Mot de passe"
              required
              autoComplete="new-password"
            />
            <input
              className="form-input"
              name="password2"
              type="password"
              placeholder="Confirmer le mot de passe"
              required
              autoComplete="new-password"
            />

            {/* Étudiant(e) */}
            {role === "student" && (
              <>
                <div
                  style={{
                    display: "grid",
                    gap: 8,
                    gridTemplateColumns: "1fr 1fr",
                  }}
                >
                  <input
                    className="form-input"
                    name="first_name"
                    placeholder="Prénom"
                    required
                    autoComplete="off"
                  />
                  <input
                    className="form-input"
                    name="last_name"
                    placeholder="Nom"
                    required
                    autoComplete="off"
                  />
                </div>
                <input
                  className="form-input"
                  name="date_of_birth"
                  type="date"
                  placeholder="Date de naissance"
                  required
                  autoComplete="off"
                />
                <input
                  className="form-input"
                  name="parent_phone"
                  placeholder="Téléphone parent"
                  required
                  autoComplete="off"
                />
                <input
                  className="form-input"
                  name="student_phone"
                  placeholder="Téléphone étudiant"
                  autoComplete="off"
                />
                <input
                  className="form-input"
                  name="parent_email"
                  type="email"
                  placeholder="Email parent"
                  autoComplete="off"
                />

                <label>Classe</label>
                <select
                  className="form-select"
                  name="classroom"
                  required
                  defaultValue=""
                >
                  <option value="" disabled>
                    — Choisir une classe —
                  </option>
                  {loadingClasses && <option disabled>Chargement…</option>}
                  {!loadingClasses &&
                    classes.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                </select>

                <label>
                  Extrait de naissance (PDF){" "}
                  <input
                    className="form-input"
                    name="birth_certificate"
                    type="file"
                    accept="application/pdf"
                  />
                </label>
                <label>
                  Dernier bulletin (PDF){" "}
                  <input
                    className="form-input"
                    name="last_school_report"
                    type="file"
                    accept="application/pdf"
                  />
                </label>
              </>
            )}

            {/* Professeur(e) */}
            {role === "professor" && (
              <>
                <div
                  style={{
                    display: "grid",
                    gap: 8,
                    gridTemplateColumns: "1fr 1fr",
                  }}
                >
                  <input
                    className="form-input"
                    name="first_name"
                    placeholder="Prénom"
                    required
                    autoComplete="off"
                  />
                  <input
                    className="form-input"
                    name="last_name"
                    placeholder="Nom"
                    required
                    autoComplete="off"
                  />
                </div>
                <input
                  className="form-input"
                  name="department"
                  placeholder="Département"
                  required
                  autoComplete="off"
                />
                <input
                  className="form-input"
                  name="hire_date"
                  type="date"
                  placeholder="Date d’embauche"
                  required
                  autoComplete="off"
                />

                <label>Programme</label>
                <select
                  className="form-select"
                  name="program"
                  required
                  defaultValue=""
                >
                  <option value="" disabled>
                    — Choisir un programme —
                  </option>
                  {loadingPrograms && <option disabled>Chargement…</option>}
                  {!loadingPrograms &&
                    programs.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name}
                      </option>
                    ))}
                </select>

                <label>Matières</label>
                <select className="form-select" name="subjects" multiple required>
                  {loadingSubjects && <option disabled>Chargement…</option>}
                  {!loadingSubjects &&
                    subjects.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.name}
                      </option>
                    ))}
                </select>
              </>
            )}

            {/* Ancien/Ancienne */}
            {role === "alumni" && (
              <>
                <div
                  style={{
                    display: "grid",
                    gap: 8,
                    gridTemplateColumns: "1fr 1fr",
                  }}
                >
                  <input
                    className="form-input"
                    name="first_name"
                    placeholder="Prénom"
                    required
                    autoComplete="off"
                  />
                  <input
                    className="form-input"
                    name="last_name"
                    placeholder="Nom"
                    required
                    autoComplete="off"
                  />
                </div>
                <input
                  className="form-input"
                  name="year_left"
                  type="number"
                  min="1950"
                  max="2100"
                  placeholder="Année de sortie"
                  required
                  autoComplete="off"
                />
                <input
                  className="form-input"
                  name="promo_name"
                  placeholder="Nom de la promo"
                  required
                  autoComplete="off"
                />
                <input
                  className="form-input"
                  name="years_interval"
                  placeholder="Intervalle d’années (ex: 2018-2025)"
                  required
                  autoComplete="off"
                />
                <label>
                  Justificatif (PDF){" "}
                  <input
                    className="form-input"
                    name="proof_document"
                    type="file"
                    accept="application/pdf"
                  />
                </label>
              </>
            )}

            <button type="submit" className="form-button">
              Valider l'inscription
            </button>

            {msg && (
              <div className="alert-message alert-success">
                ✅ {msg}
              </div>
            )}

            {err && (
              <div className="alert-message alert-error">
                ⚠️ {typeof err === "string" ? err : JSON.stringify(err)}
              </div>
            )}
          </form>
        )}
      </div>
      <FooterPage />
    </>
  );
}
