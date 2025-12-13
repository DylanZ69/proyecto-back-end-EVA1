import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet, apiPost, apiPut, apiDelete } from "../api.js";

const initialForm = {
  nombre: "",
  direccion: "",
  telefono: "",
};

export default function Refugios() {
  const [refugios, setRefugios] = useState([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const [msg, setMsg] = useState("");

  async function cargarRefugios() {
    setLoading(true);
    setMsg("");
    const res = await apiGet("/refugios/");
    const data = await res.json().catch(() => []);
    if (res.ok) setRefugios(Array.isArray(data) ? data : []);
    else setMsg("Error al cargar refugios.");
    setLoading(false);
  }

  useEffect(() => {
    cargarRefugios();
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
    if (!form.direccion.trim()) return "Dirección es obligatoria.";
    if (!form.telefono.trim()) return "Teléfono es obligatorio.";
    // Validación simple (puedes quitarla si el profe no pidió formato)
    if (form.telefono.trim().length < 6) return "Teléfono muy corto.";
    return "";
  }

  async function crearRefugio(e) {
    e.preventDefault();
    setMsg("");

    const error = validar();
    if (error) return setMsg(error);

    const payload = {
      nombre: form.nombre.trim(),
      direccion: form.direccion.trim(),
      telefono: form.telefono.trim(),
    };

    const res = await apiPost("/refugios/", payload);
    if (res.ok) {
      setMsg("Refugio creado ✅");
      resetForm();
      await cargarRefugios();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al crear refugio. " + (data?.detail || ""));
    }
  }

  async function actualizarRefugio(e) {
    e.preventDefault();
    setMsg("");

    const error = validar();
    if (error) return setMsg(error);

    const payload = {
      nombre: form.nombre.trim(),
      direccion: form.direccion.trim(),
      telefono: form.telefono.trim(),
    };

    const res = await apiPut(`/refugios/${editingId}/`, payload);
    if (res.ok) {
      setMsg("Refugio actualizado ✅");
      resetForm();
      await cargarRefugios();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al actualizar refugio. " + (data?.detail || ""));
    }
  }

  function startEdit(r) {
    setMsg("");
    setEditingId(r.id);
    setForm({
      nombre: r.nombre ?? "",
      direccion: r.direccion ?? "",
      telefono: r.telefono ?? "",
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function eliminarRefugio(id) {
    setMsg("");
    const ok = confirm("¿Eliminar este refugio?");
    if (!ok) return;

    const res = await apiDelete(`/refugios/${id}/`);
    if (res.ok) {
      setMsg("Refugio eliminado ✅");
      await cargarRefugios();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al eliminar refugio. " + (data?.detail || ""));
    }
  }

  return (
    <div style={{ maxWidth: 950, margin: "40px auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
        <h2>Refugios</h2>
        <Link to="/menu">Volver al menú</Link>
      </div>

      {msg && <p style={{ color: msg.includes("✅") ? "green" : "red" }}>{msg}</p>}

      {/* FORM */}
      <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 14, marginBottom: 16 }}>
        <h3 style={{ marginTop: 0 }}>{editingId ? "Editar Refugio" : "Crear Refugio"}</h3>

        <form onSubmit={editingId ? actualizarRefugio : crearRefugio}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <div>
              <label>Nombre</label>
              <input name="nombre" value={form.nombre} onChange={onChange} />
            </div>

            <div>
              <label>Teléfono</label>
              <input name="telefono" value={form.telefono} onChange={onChange} />
            </div>

            <div style={{ gridColumn: "1 / -1" }}>
              <label>Dirección</label>
              <input name="direccion" value={form.direccion} onChange={onChange} />
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
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Dirección</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Teléfono</th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {refugios.map((r) => (
              <tr key={r.id}>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{r.nombre}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{r.direccion}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{r.telefono}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>
                  <button onClick={() => startEdit(r)} style={{ marginRight: 8 }}>
                    Editar
                  </button>
                  <button onClick={() => eliminarRefugio(r.id)}>Eliminar</button>
                </td>
              </tr>
            ))}
            {refugios.length === 0 && (
              <tr>
                <td colSpan={4} style={{ padding: 10 }}>
                  No hay refugios registrados.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
