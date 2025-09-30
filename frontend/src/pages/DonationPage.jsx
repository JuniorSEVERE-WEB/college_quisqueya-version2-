// frontend/src/pages/DonationPage.jsx
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";

export function DonationPage() {
  return (
    <>
      <HeaderPage />
      <div style={{ padding: "50px 20px", textAlign: "center", background: "#f5f9f8", minHeight: "70vh" }}>
        <h1 style={{ fontSize: "2.4rem", marginBottom: "15px", fontWeight: "bold", color: "rgb(1,1,32)" }}>
           Faire un Don
        </h1>
        <p style={{ maxWidth: "700px", margin: "0 auto 40px auto", fontSize: "1.1rem", lineHeight: "1.6", color: "#333" }}>
          Votre soutien contribue à l’excellence et à la réussite des élèves du Collège Quisqueya de Léogâne.  
          Vous pouvez effectuer un don facilement via nos partenaires de paiement.
        </p>

        <div style={{ display: "flex", justifyContent: "center", gap: "40px", flexWrap: "wrap", marginBottom: "30px" }}>
          {/* MonCash */}
          <div style={{ background: "white", padding: "20px", borderRadius: "12px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}>
            <img 
              src="/logo-moncash.png" 
              alt="MonCash" 
              style={{ width: "140px", height: "auto", display: "block", margin: "0 auto" }} 
            />
            <p style={{ marginTop: "10px", color: "rgb(1,1,32)", fontWeight: "bold" }}>MonCash (Haïti)</p>
          </div>

          {/* MasterCard */}
          <div style={{ background: "white", padding: "20px", borderRadius: "12px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)" }}>
            <img 
              src="/logo-mastercard.png" 
              alt="MasterCard" 
              style={{ width: "140px", height: "auto", display: "block", margin: "0 auto" }} 
            />
            <p style={{ marginTop: "10px", color: "rgb(1,1,32)", fontWeight: "bold" }}>Carte bancaire (MasterCard)</p>
          </div>
        </div>

        <p style={{ marginTop: "20px", fontSize: "0.95rem", color: "#444", fontStyle: "italic" }}>
          ℹ️ Cette page est une démonstration statique. Les paiements en ligne seront bientôt disponibles.
        </p>
      </div>
      <FooterPage />
    </>
  );
}
