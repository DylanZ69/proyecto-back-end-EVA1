import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { clearToken } from "../api.js";

export default function Menu() {
  const navigate = useNavigate();

  function logout() {
    clearToken();
    navigate("/login");
  }

  return (
    <div style={{ maxWidth: 800, margin: "40px auto" }}>
      <h2>Menú</h2>

      <nav style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <Link to="/mascotas">Mascotas</Link>
        <Link to="/refugios">Refugios</Link>
        <Link to="/solicitudes">Solicitudes</Link>
        <button onClick={logout}>Cerrar sesión</button>
      </nav>
    </div>
  );
}
