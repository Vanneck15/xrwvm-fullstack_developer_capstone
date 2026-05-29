import React, { useState, useEffect } from "react";
import { Routes, Route, Link } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";
import Dealers from './components/Dealers/Dealers';

function App() {
  const [username, setUsername] = useState(null);

  // Vérifie si un utilisateur est connecté au chargement de la page
  useEffect(() => {
    const storedUsername = sessionStorage.getItem("username");
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);

  // Fonction pour se déconnecter
  const logout = () => {
    sessionStorage.removeItem("username");
    setUsername(null);
    window.location.href = window.location.origin;
  };

  return (
    <div>
      {/* Barre de navigation supérieure (Navbar turquoise) */}
      <nav className="navbar" style={{
        backgroundColor: "#22d3ee", 
        padding: "15px 30px", 
        display: "flex", 
        justifyContent: "space-between", 
        alignItems: "center"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "40px" }}>
          <h1 style={{ margin: 0, fontSize: "28px", fontWeight: "bold", color: "#0f172a" }}>
            Dealerships
          </h1>
          <div style={{ display: "flex", gap: "20px", fontSize: "18px" }}>
            <Link to="/" style={{ textDecoration: "none", color: "#0f172a" }}>Home</Link>
            <Link to="/about" style={{ textDecoration: "none", color: "#475569" }}>About Us</Link>
            <Link to="/contact" style={{ textDecoration: "none", color: "#475569" }}>Contact Us</Link>
          </div>
        </div>

        {/* Section Connexion / Déconnexion dynamique */}
        <div style={{ fontSize: "18px", fontWeight: "500" }}>
          {username ? (
            <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
              <span style={{ color: "#0f172a" }}>{username}</span>
              <button onClick={logout} style={{
                background: "none",
                border: "none",
                color: "#0f172a",
                cursor: "pointer",
                fontSize: "18px",
                textDecoration: "underline"
              }}>
                Logout
              </button>
            </div>
          ) : (
            <div style={{ display: "flex", gap: "20px" }}>
              <Link to="/login" style={{ textDecoration: "none", color: "#0f172a" }}>Login</Link>
              <Link to="/register" style={{ textDecoration: "none", color: "#0f172a" }}>Register</Link>
            </div>
          )}
        </div>
      </nav>

      {/* Contenu des routes sous la Navbar */}
      <div style={{ padding: "20px" }}>
        <Routes>
          {/* Par défaut, la racine "/" affiche la liste des concessionnaires */}
          <Route path="/" element={<Dealers />} />
          <Route path="/login" element={<LoginPanel />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dealers" element={<Dealers />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;