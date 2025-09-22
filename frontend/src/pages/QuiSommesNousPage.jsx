import { HeaderPage } from '../components/HeaderPage';
import { FooterPage } from '../components/FooterPage';

export default function QuiSommesNousPage() {
  return (
    <>
      <HeaderPage />
      <div className="qui-sommes-nous-page">
        <h2>Qui sommes-nous ?</h2>
        <p>Bienvenue sur la page de présentation de l'école Quisqueya. Ici, vous pouvez ajouter une description de l'établissement, son histoire, sa mission, ses valeurs, etc.</p>
      </div>
      <FooterPage />
    </>
  );
}
