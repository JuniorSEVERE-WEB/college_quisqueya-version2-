import { useState } from "react";
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
export default function ContactPage() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [sent, setSent] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSent(true);
    // Ici tu pourrais envoyer les données à un backend plus tard
  };

  if (sent) {
    return (
      <div style={{ color: "green" }}>
        Merci pour votre message ! Nous vous répondrons bientôt.
      </div>
    );
  }

  return (
    <>
    <HeaderPage />
      <div className="contact-page">
        <h2>Contact</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Votre nom"
            value={form.name}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Votre email"
            value={form.email}
            onChange={handleChange}
            required
          />
          <textarea
            name="message"
            placeholder="Votre message"
            value={form.message}
            onChange={handleChange}
            required
          />
          <button type="submit">Envoyer</button>
        </form>
      </div>
      <FooterPage />
    </>
  );
}
