import React, { useEffect, useState } from "react";
import API from "../api";
import "./dashboard.css";

export function StudentsManager() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState(null); // Élève en cours d’édition
  const [form, setForm] = useState({});

  // 1️⃣ Charger les élèves
  useEffect(() => {
    API.get("students/") // ✅ bon endpoint
      .then((res) => {
        console.log("✅ Données reçues :", res.data);

        // ✅ Certains DRF renvoient { results: [...] }
        if (Array.isArray(res.data)) {
          setStudents(res.data);
        } else if (Array.isArray(res.data.results)) {
          setStudents(res.data.results);
        } else {
          setStudents([]);
        }

        setLoading(false);
      })
      .catch((err) => {
        console.error("❌ Erreur API :", err);
        setError("Impossible de charger les élèves.");
        setLoading(false);
      });
  }, []);

  // 2️⃣ Supprimer un élève
  const handleDelete = async (id) => {
    if (!window.confirm("Supprimer cet élève ?")) return;
    try {
      await API.delete(`students/${id}/`); // ✅ bon endpoint
      setStudents((prev) => prev.filter((s) => s.id !== id));
    } catch (err) {
      alert("Erreur lors de la suppression.");
      console.error(err);
    }
  };

  // 3️⃣ Modifier un élève
  const startEdit = (student) => {
    setEditing(student.id);
    setForm({
      first_name: student.user?.first_name || "",
      last_name: student.user?.last_name || "",
      parent_phone: student.parent_phone || "",
    });
  };

  const handleEditChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = async (id) => {
    try {
      await API.patch(`students/${id}/`, form); // ✅ bon endpoint
      alert("✅ Élève mis à jour !");
      setEditing(null);

      // Recharge les élèves
      const res = await API.get("students/");
      setStudents(Array.isArray(res.data) ? res.data : res.data.results || []);
    } catch (err) {
      alert("Erreur lors de la mise à jour.");
      console.error(err);
    }
  };

  if (loading) return <p>Chargement...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="dashboard-container">
      <h2>👩‍🎓 Gestion des élèves</h2>

      <table className="students-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nom complet</th>
            <th>Téléphone parent</th>
            <th>Classe</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {students.length > 0 ? (
            students.map((student) => (
              <tr key={student.id}>
                <td>{student.id}</td>
                <td>
                  {editing === student.id ? (
                    <>
                      <input
                        type="text"
                        name="first_name"
                        value={form.first_name}
                        onChange={handleEditChange}
                        placeholder="Prénom"
                      />
                      <input
                        type="text"
                        name="last_name"
                        value={form.last_name}
                        onChange={handleEditChange}
                        placeholder="Nom"
                      />
                    </>
                  ) : (
                    `${student.user?.first_name || ""} ${student.user?.last_name || ""}`
                  )}
                </td>
                <td>
                  {editing === student.id ? (
                    <input
                      type="text"
                      name="parent_phone"
                      value={form.parent_phone}
                      onChange={handleEditChange}
                    />
                  ) : (
                    student.parent_phone || "—"
                  )}
                </td>
                <td>{student.classroom_name || student.classroom || "—"}</td>
                <td>
                  {editing === student.id ? (
                    <button onClick={() => handleSave(student.id)}>💾 Save</button>
                  ) : (
                    <>
                      <button onClick={() => startEdit(student)}>✏️ Edit</button>
                      <button onClick={() => handleDelete(student.id)}>🗑️ Delete</button>
                    </>
                  )}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5">Aucun élève trouvé.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
