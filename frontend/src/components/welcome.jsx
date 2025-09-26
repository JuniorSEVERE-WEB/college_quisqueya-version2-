// Bienvenue.jsx
import React from "react";
import "./welcome.css";

export default function Bienvenue() {
  return (
    <section className="welcome-section">
      <div className="container">
        <h1 className="welcome-title">Bienvenue au Collège Quisqueya</h1>
        <p className="welcome-text">
          Le Collège Quisqueya est un établissement d’enseignement moderne et
          dynamique, engagé à offrir à chaque élève un cadre éducatif stimulant
          et bienveillant. Nous formons des citoyens responsables, créatifs et
          ouverts sur le monde, en alliant rigueur académique et développement
          personnel.
          <br />
          Notre mission est de cultiver l’excellence, la discipline et l’éthique,
          afin que chaque apprenant puisse s’épanouir et réaliser son plein
          potentiel.
        </p>
      </div>
    </section>
  );
}
