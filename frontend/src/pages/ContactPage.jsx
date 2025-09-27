import React, { useState } from "react";
import API from "../api"; // ton instance Axios
import { HeaderPage } from "../components/HeaderPage";
import { FooterPage } from "../components/FooterPage";
import "./contact.css";

export function ContactPage() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  const [status, setStatus] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("/contact-messages/", form);
      setStatus("✅ Message envoyé avec succès !");
      setForm({ name: "", email: "", subject: "", message: "" });
    } catch (error) {
      console.error(error);
      setStatus("❌ Erreur lors de l’envoi du message.");
    }
  };

  return (
    <>
      <HeaderPage />

      <div className="contact-container">
        <h1>Contactez-nous</h1>
        {status && <p className="status-message">{status}</p>}

        <form onSubmit={handleSubmit} className="contact-form">
          <label>
            Nom :
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Email :
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Sujet :
            <input
              type="text"
              name="subject"
              value={form.subject}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Message :
            <textarea
              name="message"
              value={form.message}
              onChange={handleChange}
              required
            />
          </label>

          <button type="submit">Envoyer</button>
        </form>
      </div>

      <FooterPage />
    </>
  );
}
