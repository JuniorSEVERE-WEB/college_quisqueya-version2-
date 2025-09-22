import { useState } from 'react';
import API from '../api';
import { useNavigate } from 'react-router-dom';
import { HeaderPage } from '../components/HeaderPage';
import { FooterPage } from '../components/FooterPage';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('student');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await API.post('register/', { username, password, role });
      setSuccess('Inscription réussie ! Vous pouvez vous connecter.');
      setTimeout(() => navigate('/login'), 1500);
    } catch (err) {
      setError("Erreur lors de l'inscription");
    }
  };

  return (
    <>
      <HeaderPage />
      <div className="register-page">
        <h2>Inscription</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
          placeholder="Nom d'utilisateur"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Mot de passe"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="student">Étudiant</option>
          <option value="teacher">Enseignant</option>
          <option value="employee">Employé</option>
        </select>
        <button type="submit">S'inscrire</button>
      </form>
      {error && <div style={{color:'red'}}>{error}</div>}
      {success && <div style={{color:'green'}}>{success}</div>}
    </div>
    <FooterPage />
    </>
  );
}
