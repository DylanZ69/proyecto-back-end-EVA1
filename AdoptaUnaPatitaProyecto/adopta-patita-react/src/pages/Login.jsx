import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiPost, setToken } from "../api.js";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setMsg("");

    if (!username || !password) {
      setMsg("Completa usuario y contraseña.");
      return;
    }

    const res = await apiPost("/token/", { username, password });
    const data = await res.json().catch(() => ({}));

    if (res.ok && data.token) {
      setToken(data.token);
      navigate("/menu");
    } else {
      setMsg("Credenciales incorrectas.");
    }
  }

  return (
    <div style={{ maxWidth: 420, margin: "40px auto" }}>
      <h2>Login</h2>
      {msg && <p style={{ color: "red" }}>{msg}</p>}

      <form onSubmit={handleSubmit}>
        <label>Usuario</label>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="usuario"
        />

        <label>Contraseña</label>
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="contraseña"
          type="password"
        />

        <button type="submit">Ingresar</button>
      </form>
    </div>
  );
}
