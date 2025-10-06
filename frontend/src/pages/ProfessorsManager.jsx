import React, { useEffect, useState } from "react";
import API from "../api";
import "./dashboard.css";
import "./professorsmanagers.css";

export function ProfessorsManager() {
  const [professors, setProfessors] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({});
  const [selected, setSelected] = useState([]); // ✅ sélection multiple
  const [search, setSearch] = useState("");

  // Charger les professeurs
  useEffect(() => {
    API.get("professors/")
      .then((res) => {
        const data = Array.isArray(res.data)
          ? res.data
          : res.data.results || [];
        setProfessors(data);
        setFiltered(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("❌ Erreur API :", err);
        setError("Impossible de charger les professeurs.");
        setLoading(false);
      });
  }, []);

  // 🔎 Recherche en temps réel
  useEffect(() => {
    if (!search.trim()) {
      setFiltered(professors);
      return;
    }
    const lower = search.toLowerCase();
    const filteredData = professors.filter(
      (p) =>
        p.user?.first_name?.toLowerCase().includes(lower) ||
        p.user?.last_name?.toLowerCase().includes(lower) ||
        p.department?.toLowerCase().includes(lower) ||
        p.subjects?.join(", ").toLowerCase().includes(lower)
    );
    setFiltered(filteredData);
  }, [search, professors]);

  // ✅ Ajouter un professeur vide (ligne d’ajout)
  const handleAdd = () => {
    const newProf = {
      id: Date.now(),
      user: { first_name: "", last_name: "" },
      department: "",
      subjects: [],
      hire_date: "",
      academic_year: "2025-2026",
      isNew: true,
    };
    setProfessors([newProf, ...professors]);
    setFiltered([newProf, ...filtered]);
    setEditing(newProf.id);
    setForm({
      first_name: "",
      last_name: "",
      department: "",
      hire_date: "",
    });
  };

  // ✅ Sélectionner / désélectionner un prof
  const toggleSelect = (id) => {
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]
    );
  };

  // ✅ Supprimer plusieurs professeurs
  const handleBulkDelete = async () => {
    if (selected.length === 0) {
      alert("Aucun professeur sélectionné.");
      return;
    }
    if (!window.confirm(`Supprimer ${selected.length} professeur(s) ?`)) return;

    try {
      await Promise.all(selected.map((id) => API.delete(`professors/${id}/`)));
      setProfessors((prev) => prev.filter((p) => !selected.includes(p.id)));
      setFiltered((prev) => prev.filter((p) => !selected.includes(p.id)));
      setSelected([]);
      alert("✅ Suppression multiple réussie !");
    } catch (err) {
      console.error("Erreur suppression multiple :", err);
      alert("Erreur lors de la suppression.");
    }
  };

  const startEdit = (professor) => {
    setEditing(professor.id);
    setForm({
      first_name: professor.user?.first_name || "",
      last_name: professor.user?.last_name || "",
      department: professor.department || "",
      hire_date: professor.hire_date || "",
    });
  };

  const handleEditChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ✅ Enregistrer ou créer un professeur
  const handleSave = async (id) => {
    try {
      if (professors.find((p) => p.id === id && p.isNew)) {
        // POST - nouveau prof
        await API.post("professors/", form);
        alert("✅ Nouveau professeur ajouté !");
      } else {
        // PATCH - modification
        await API.patch(`professors/${id}/`, form);
        alert("✅ Professeur mis à jour !");
      }

      // Recharge la liste
      const res = await API.get("professors/");
      const data = Array.isArray(res.data)
        ? res.data
        : res.data.results || [];
      setProfessors(data);
      setFiltered(data);
      setEditing(null);
    } catch (err) {
      console.error(err);
      alert("Erreur lors de l’enregistrement.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Supprimer ce professeur ?")) return;
    try {
      await API.delete(`professors/${id}/`);
      setProfessors((prev) => prev.filter((p) => p.id !== id));
      setFiltered((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      alert("Erreur lors de la suppression.");
      console.error(err);
    }
  };

  if (loading) return <p>Chargement...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="dashboard-container">
      <div className="header-tools">
        <h2>👨‍🏫 Gestion des professeurs</h2>
        <div className="actions">
          <input
            type="text"
            placeholder="🔍 Rechercher..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
         
        </div>
      </div>

      <table className="students-table">
        <thead>
          <tr>
            <th>
              <input
                type="checkbox"
                checked={
                  selected.length > 0 && selected.length === filtered.length
                }
                onChange={(e) =>
                  e.target.checked
                    ? setSelected(filtered.map((p) => p.id))
                    : setSelected([])
                }
              />
            </th>
            <th>ID</th>
            <th>Prénom</th>
            <th>Nom</th>
            <th>Département</th>
            <th>Matières</th>
            <th>Date d’embauche</th>
            <th>Année académique</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filtered.length > 0 ? (
            filtered.map((p) => (
              <tr key={p.id}>
                <td>
                  <input
                    type="checkbox"
                    checked={selected.includes(p.id)}
                    onChange={() => toggleSelect(p.id)}
                  />
                </td>
                <td>{p.id}</td>

                {editing === p.id ? (
                  <>
                    <td>
                      <input
                        name="first_name"
                        value={form.first_name}
                        onChange={handleEditChange}
                      />
                    </td>
                    <td>
                      <input
                        name="last_name"
                        value={form.last_name}
                        onChange={handleEditChange}
                      />
                    </td>
                    <td>
                      <input
                        name="department"
                        value={form.department}
                        onChange={handleEditChange}
                      />
                    </td>
                    <td>—</td>
                    <td>
                      <input
                        type="date"
                        name="hire_date"
                        value={form.hire_date}
                        onChange={handleEditChange}
                      />
                    </td>
                    <td>{p.academic_year || "—"}</td>
                    <td>
                      <button onClick={() => handleSave(p.id)}>💾 Save</button>
                      <button onClick={() => setEditing(null)}>❌ Cancel</button>
                    </td>
                  </>
                ) : (
                  <>
                    <td>{p.user?.first_name || "—"}</td>
                    <td>{p.user?.last_name || "—"}</td>
                    <td>{p.department || "—"}</td>
                    <td>
                      {p.subjects?.length
                        ? p.subjects.join(", ")
                        : "Aucune matière"}
                    </td>
                    <td>{p.hire_date || "—"}</td>
                    <td>{p.academic_year || "—"}</td>
                    <td>
                      <button onClick={() => startEdit(p)}>✏️ Edit</button>
                      <button onClick={() => handleDelete(p.id)}>🗑️ Delete</button>
                    </td>
                  </>
                )}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="9">Aucun professeur trouvé.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
