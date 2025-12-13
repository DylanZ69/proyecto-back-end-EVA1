import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login.jsx";
import Menu from "./pages/Menu.jsx";
import Mascotas from "./pages/Mascotas.jsx";
import Refugios from "./pages/Refugios.jsx";
import Solicitudes from "./pages/Solicitudes.jsx";
import { getToken } from "./api.js";

function PrivateRoute({ children }) {
  const token = getToken();
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/menu" replace />} />
      <Route path="/login" element={<Login />} />

      <Route
        path="/menu"
        element={
          <PrivateRoute>
            <Menu />
          </PrivateRoute>
        }
      />
      <Route
        path="/mascotas"
        element={
          <PrivateRoute>
            <Mascotas />
          </PrivateRoute>
        }
      />
      <Route
        path="/refugios"
        element={
          <PrivateRoute>
            <Refugios />
          </PrivateRoute>
        }
      />
      <Route
        path="/solicitudes"
        element={
          <PrivateRoute>
            <Solicitudes />
          </PrivateRoute>
        }
      />
    </Routes>
  );
}
