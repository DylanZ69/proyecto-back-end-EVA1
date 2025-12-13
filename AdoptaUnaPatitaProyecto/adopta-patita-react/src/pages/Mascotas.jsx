import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet, apiPost, apiPut, apiDelete } from "../api.js";

const initialForm = {
  nombre: "",
  edad: "",
  raza: "",
  tipo: "",
  refugio_nombre: "",
};

export default function Mascotas() {
  const [mascotas, setMascotas] = useState([]);
  const [loading, setLoading] = useState(true);

  // form create/edit
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const [msg, setMsg] = useState("");

  async function cargarMascotas() {
    setLoading(true);
    setMsg("");
    const res = await apiGet("/mascotas/");
    const data = await res.json().catch(() => []);
    if (res.ok) setMascotas(Array.isArray(data) ? data : []);
    else setMsg("Error al cargar mascotas.");
    setLoading(false);
  }

  useEffect(() => {
    cargarMascotas();
  }, []);

  function onChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function resetForm() {
    setForm(initialForm);
    setEditingId(null);
  }

  function validar() {
    if (!form.nombre.trim()) return "Nombre es obligatorio.";
    if (form.edad === "" || isNaN(Number(form.edad))) return "Edad debe ser numérica.";
    if (!form.raza.trim()) return "Raza es obligatoria.";
    if (!form.tipo.trim()) return "Tipo es obligatorio.";
    if (!form.refugio_nombre.trim()) return "Refugio (nombre) es obligatorio.";
    return "";
  }

  async function crearMascota(e) {
    e.preventDefault();
    setMsg("");

    const error = validar();
    if (error) return setMsg(error);

    const payload = {
      nombre: form.nombre.trim(),
      edad: Number(form.edad),
      raza: form.raza.trim(),
      tipo: form.tipo.trim(),
      refugio_nombre: form.refugio_nombre.trim(),
    };

    const res = await apiPost("/mascotas/", payload);
    if (res.ok) {
      setMsg("Mascota creada ✅");
      resetForm();
      await cargarMascotas();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al crear mascota. " + (data?.detail || ""));
    }
  }

  async function actualizarMascota(e) {
    e.preventDefault();
    setMsg("");

    const error = validar();
    if (error) return setMsg(error);

    const payload = {
      nombre: form.nombre.trim(),
      edad: Number(form.edad),
      raza: form.raza.trim(),
      tipo: form.tipo.trim(),
      refugio_nombre: form.refugio_nombre.trim(),
    };

    const res = await apiPut(`/mascotas/${editingId}/`, payload);
    if (res.ok) {
      setMsg("Mascota actualizada ✅");
      resetForm();
      await cargarMascotas();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al actualizar mascota. " + (data?.detail || ""));
    }
  }

  function startEdit(m) {
    setMsg("");
    setEditingId(m.id);
    setForm({
      nombre: m.nombre ?? "",
      edad: m.edad ?? "",
      raza: m.raza ?? "",
      tipo: m.tipo ?? "",
      refugio_nombre: m.refugio_nombre ?? "",
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function eliminarMascota(id) {
    setMsg("");
    const ok = confirm("¿Eliminar esta mascota?");
    if (!ok) return;

    const res = await apiDelete(`/mascotas/${id}/`);
    if (res.ok) {
      setMsg("Mascota eliminada ✅");
      await cargarMascotas();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al eliminar mascota. " + (data?.detail || ""));
    }
  }

  return (
    <div style={{ maxWidth: 950, margin: "40px auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
        <h2>Mascotas</h2>
        <Link to="/menu">Volver al menú</Link>
      </div>

      {msg && <p style={{ color: msg.includes("✅") ? "green" : "red" }}>{msg}</p>}

      {/* FORM */}
      <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 14, marginBottom: 16 }}>
        <h3 style={{ marginTop: 0 }}>{editingId ? "Editar Mascota" : "Crear Mascota"}</h3>

        <form onSubmit={editingId ? actualizarMascota : crearMascota}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <div>
              <label>Nombre</label>
              <input name="nombre" value={form.nombre} onChange={onChange} />
            </div>

            <div>
              <label>Edad</label>
              <input name="edad" type="number" value={form.edad} onChange={onChange} />
            </div>

            <div>
              <label>Raza</label>
              <input name="raza" value={form.raza} onChange={onChange} />
            </div>

            <div>
              <label>Tipo</label>
              <input name="tipo" value={form.tipo} onChange={onChange} />
            </div>

            <div style={{ gridColumn: "1 / -1" }}>
              <label>Refugio (nombre)</label>
              <input name="refugio_nombre" value={form.refugio_nombre} onChange={onChange} />
            </div>
          </div>

          <div style={{ marginTop: 12, display: "flex", gap: 10, flexWrap: "wrap" }}>
            <button type="submit">{editingId ? "Guardar cambios" : "Crear"}</button>
            {editingId && (
              <button type="button" onClick={resetForm}>
                Cancelar edición
              </button>
            )}
          </div>
        </form>
      </div>

      {/* LISTA */}
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Nombre</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Edad</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Raza</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Tipo</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Refugio</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {mascotas.map((m) => (
              <tr key={m.id}>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{m.nombre}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{m.edad}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{m.raza}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{m.tipo}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{m.refugio_nombre}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>
                  <button onClick={() => startEdit(m)} style={{ marginRight: 8 }}>
                    Editar
                  </button>
                  <button onClick={() => eliminarMascota(m.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
            {mascotas.length === 0 && (
              <tr>
                <td colSpan={6} style={{ padding: 10 }}>
                  No hay mascotas registradas.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
