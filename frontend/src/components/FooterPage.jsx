import "./footerpage.css";

export function FooterPage() {
  return (
    <>
      <div className="foot-page">
        <div className="part1">
          <h2 className="centre">College Quisqueya de Leogane</h2>
          <p>Une plateforme qui apuie sur CS50 pour etre plus explicite</p>
        </div>
        <div className="part2">
          <h2>Menu</h2>
          <ul>
            <li>
              <a href="#">Acceuil</a>
            </li>
            <li>
              <a href="sommesnous.html">Qui sommes nous</a>
            </li>
            <li>
              <a href="mission.html">Mission</a>
            </li>
            <li>
              <a href="contact.html">Contact</a>
            </li>
            <li>
              <a href="connexion.html">Connexion</a>
            </li>
            <li>
              <a href="deconnexion.html">Deconnexion</a>
            </li>
          </ul>
        </div>
        <div className="part3">
          <h2 className="centre">Contactez-nous</h2>
          <p>#56, Leogane, Haiti</p>
          <p>collegequisqueyadeleogane@gmail.com</p>
        </div>
      </div>

      <div className="copyright-inscrire">
        <div>Copyright © 2025 Quisqueya All rights reserved</div>
        <div>
          <ul>
            <li>
              <a href="connexion.html">Connexion</a>
            </li>
            <li>
              <a href="deconnexion.html">Deconnexion</a>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
}
