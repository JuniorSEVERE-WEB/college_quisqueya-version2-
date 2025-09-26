// frontend/src/pages/RegisterPage.jsx
import { useEffect, useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import API from "../api";

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

  // reset messages à chaque changement de rôle
  useEffect(() => {
    setMsg("");
    setErr("");
  }, [role]);

  // Charger classes si étudiant
  useEffect(() => {
    if (role === "student") {
      setLoadingClasses(true);
      setClasses([]);
      API.get("classrooms/public/")
        .then(res =>
          setClasses(Array.isArray(res.data) ? res.data : (res.data?.results || []))
        )
        .catch(() => setErr("Impossible de charger les classes."))
        .finally(() => setLoadingClasses(false));
    }
  }, [role]);

  // Charger programmes & matières si professeur
  useEffect(() => {
    if (role === "professor") {
      setLoadingPrograms(true);
      setLoadingSubjects(true);
      setPrograms([]);
      setSubjects([]);

      API.get("programs/public/")
        .then(res =>
          setPrograms(Array.isArray(res.data) ? res.data : (res.data?.results || []))
        )
        .catch(() => setErr("Impossible de charger les programmes."))
        .finally(() => setLoadingPrograms(false));

      API.get("subjects/public/")
        .then(res =>
          setSubjects(Array.isArray(res.data) ? res.data : (res.data?.results || []))
        )
        .catch(() => setErr("Impossible de charger les matières."))
        .finally(() => setLoadingSubjects(false));
    }
  }, [role]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");
    setErr("");
    const form = new FormData(e.currentTarget);

    try {
      if (role === "membersite") {
        await API.post("auth/register/membersite/", {
          username: form.get("username"),
          email: form.get("email"),
          password1: form.get("password1"),
          password2: form.get("password2"),
        });
        setMsg("Compte créé. Vous pouvez vous connecter.");
      } else if (role === "student") {
        const fd = new FormData();
        [
          "username","email","password1","password2",
          "first_name","last_name","date_of_birth",
          "parent_phone","student_phone","parent_email","classroom"
        ].forEach(k => { if (form.get(k)) fd.append(k, form.get(k)); });
        if (form.get("birth_certificate")) fd.append("birth_certificate", form.get("birth_certificate"));
        if (form.get("last_school_report")) fd.append("last_school_report", form.get("last_school_report"));

        await API.post("students/register/", fd, { headers: { "Content-Type": "multipart/form-data" } });
        setMsg("Demande envoyée. En attente de validation de l’administration.");
      } else if (role === "professor") {
        const fd = new FormData();
        [
          "username","email","password1","password2",
          "first_name","last_name","department","hire_date","program"
        ].forEach(k => { if (form.get(k)) fd.append(k, form.get(k)); });
        for (let s of form.getAll("subjects")) {
          fd.append("subjects", s);
        }

        await API.post("professors/register/", fd);
        setMsg("Demande envoyée. En attente de validation de l’administration.");
      } else if (role === "alumni") {
        const fd = new FormData();
        [
          "username","email","password1","password2",
          "first_name","last_name","year_left","promo_name","years_interval"
        ].forEach(k => { if (form.get(k)) fd.append(k, form.get(k)); });
        if (form.get("proof_document")) fd.append("proof_document", form.get("proof_document"));

        await API.post("alumni/register/", fd, { headers: { "Content-Type": "multipart/form-data" } });
        setMsg("Demande envoyée. En attente de validation de l’administration.");
      }

      e.currentTarget.reset();
    } catch (e2) {
      const detail = e2?.response?.data || e2?.message || "Erreur d’inscription.";
      setErr(typeof detail === "string" ? detail : JSON.stringify(detail));
    }
  };

  return (
    <>
      <HeaderPage />
      <div style={{ maxWidth: 900, margin: "24px auto", padding: "0 16px" }}>
        <h2 style={{ textAlign: "center", marginBottom: 16 }}>S'inscrire</h2>

        {!role && (
          <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))" }}>
            <button onClick={() => setRole("membersite")}>Membre du site</button>
            <button onClick={() => setRole("student")}>Étudiant</button>
            <button onClick={() => setRole("professor")}>Professeur</button>
            <button onClick={() => setRole("alumni")}>Alumni</button>
          </div>
        )}

        {role && (
          <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12, marginTop: 12 }}>
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <strong>Type: {role}</strong>
              <button type="button" onClick={() => setRole("")} style={{ marginLeft: "auto" }}>Changer</button>
            </div>

            {/* Champs communs */}
            <input name="username" placeholder="Nom d'utilisateur" required />
            <input name="email" type="email" placeholder="Email" required />
            <input name="password1" type="password" placeholder="Mot de passe" required />
            <input name="password2" type="password" placeholder="Confirmer le mot de passe" required />

            {/* Étudiant */}
            {role === "student" && (
              <>
                <div style={{ display: "grid", gap: 8, gridTemplateColumns: "1fr 1fr" }}>
                  <input name="first_name" placeholder="Prénom" required />
                  <input name="last_name" placeholder="Nom" required />
                </div>
                <input name="date_of_birth" type="date" placeholder="Date de naissance" required />
                <input name="parent_phone" placeholder="Téléphone parent" required />
                <input name="student_phone" placeholder="Téléphone étudiant" />
                <input name="parent_email" type="email" placeholder="Email parent" />

                <label>Classe</label>
                <select name="classroom" required defaultValue="">
                  <option value="" disabled>— Choisir une classe —</option>
                  {loadingClasses && <option disabled>Chargement…</option>}
                  {!loadingClasses && classes.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>

                <label>Extrait de naissance (PDF) <input name="birth_certificate" type="file" accept="application/pdf" /></label>
                <label>Dernier bulletin (PDF) <input name="last_school_report" type="file" accept="application/pdf" /></label>
              </>
            )}

            {/* Professeur */}
            {role === "professor" && (
              <>
                <div style={{ display: "grid", gap: 8, gridTemplateColumns: "1fr 1fr" }}>
                  <input name="first_name" placeholder="Prénom" required />
                  <input name="last_name" placeholder="Nom" required />
                </div>
                <input name="department" placeholder="Département" required />
                <input name="hire_date" type="date" placeholder="Date d’embauche" required />

                <label>Programme</label>
                <select name="program" required defaultValue="">
                  <option value="" disabled>— Choisir un programme —</option>
                  {loadingPrograms && <option disabled>Chargement…</option>}
                  {!loadingPrograms && programs.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>

                <label>Matières</label>
                <select name="subjects" multiple required>
                  {loadingSubjects && <option disabled>Chargement…</option>}
                  {!loadingSubjects && subjects.map(s => (
                    <option key={s.id} value={s.id}>{s.name}</option>
                  ))}
                </select>
              </>
            )}

            {/* Alumni */}
            {role === "alumni" && (
              <>
                <div style={{ display: "grid", gap: 8, gridTemplateColumns: "1fr 1fr" }}>
                  <input name="first_name" placeholder="Prénom" required />
                  <input name="last_name" placeholder="Nom" required />
                </div>
                <input name="year_left" type="number" min="1950" max="2100" placeholder="Année de sortie" required />
                <input name="promo_name" placeholder="Nom de la promo" required />
                <input name="years_interval" placeholder="Intervalle d’années (ex: 2018-2025)" required />
                <label>Justificatif (PDF) <input name="proof_document" type="file" accept="application/pdf" /></label>
              </>
            )}

            <button type="submit">Valider l'inscription</button>
            {msg && <div style={{ color: "green" }}>{msg}</div>}
            {err && <div style={{ color: "red" }}>{err}</div>}
          </form>
        )}
      </div>
      <FooterPage />
    </>
  );
}
