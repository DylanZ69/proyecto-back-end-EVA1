import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiGet, apiPost, apiPut, apiDelete } from "../api.js";

const initialForm = {
  nombre_adoptante: "",
  correo: "",
  mascota_nombre: "",
};

export default function Solicitudes() {
  const [solicitudes, setSolicitudes] = useState([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);

  const [msg, setMsg] = useState("");

  async function cargarSolicitudes() {
    setLoading(true);
    setMsg("");
    const res = await apiGet("/solicitudes/");
    const data = await res.json().catch(() => []);
    if (res.ok) setSolicitudes(Array.isArray(data) ? data : []);
    else setMsg("Error al cargar solicitudes.");
    setLoading(false);
  }

  useEffect(() => {
    cargarSolicitudes();
  }, []);

  function onChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function resetForm() {
    setForm(initialForm);
    setEditingId(null);
  }

  function validar() {
    if (!form.nombre_adoptante.trim()) return "Nombre del adoptante es obligatorio.";
    if (!form.correo.trim()) return "Correo es obligatorio.";
    // validación simple email
    if (!form.correo.includes("@") || !form.correo.includes(".")) return "Correo no válido.";
    if (!form.mascota_nombre.trim()) return "Nombre de mascota es obligatorio.";
    return "";
  }

  async function crearSolicitud(e) {
    e.preventDefault();
    setMsg("");

    const error = validar();
    if (error) return setMsg(error);

    const payload = {
      nombre_adoptante: form.nombre_adoptante.trim(),
      correo: form.correo.trim(),
      mascota_nombre: form.mascota_nombre.trim(),
    };

    const res = await apiPost("/solicitudes/", payload);
    if (res.ok) {
      setMsg("Solicitud creada ✅");
      resetForm();
      await cargarSolicitudes();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al crear solicitud. " + (data?.detail || ""));
    }
  }

  async function actualizarSolicitud(e) {
    e.preventDefault();
    setMsg("");

    const error = validar();
    if (error) return setMsg(error);

    const payload = {
      nombre_adoptante: form.nombre_adoptante.trim(),
      correo: form.correo.trim(),
      mascota_nombre: form.mascota_nombre.trim(),
    };

    const res = await apiPut(`/solicitudes/${editingId}/`, payload);
    if (res.ok) {
      setMsg("Solicitud actualizada ✅");
      resetForm();
      await cargarSolicitudes();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al actualizar solicitud. " + (data?.detail || ""));
    }
  }

  function startEdit(s) {
    setMsg("");
    setEditingId(s.id);
    setForm({
      nombre_adoptante: s.nombre_adoptante ?? "",
      correo: s.correo ?? "",
      mascota_nombre: s.mascota_nombre ?? "",
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function eliminarSolicitud(id) {
    setMsg("");
    const ok = confirm("¿Eliminar esta solicitud?");
    if (!ok) return;

    const res = await apiDelete(`/solicitudes/${id}/`);
    if (res.ok) {
      setMsg("Solicitud eliminada ✅");
      await cargarSolicitudes();
    } else {
      const data = await res.json().catch(() => ({}));
      setMsg("Error al eliminar solicitud. " + (data?.detail || ""));
    }
  }

  return (
    <div style={{ maxWidth: 950, margin: "40px auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
        <h2>Solicitudes</h2>
        <Link to="/menu">Volver al menú</Link>
      </div>

      {msg && <p style={{ color: msg.includes("✅") ? "green" : "red" }}>{msg}</p>}

      {/* FORM */}
      <div style={{ border: "1px solid #ddd", borderRadius: 10, padding: 14, marginBottom: 16 }}>
        <h3 style={{ marginTop: 0 }}>{editingId ? "Editar Solicitud" : "Crear Solicitud"}</h3>

        <form onSubmit={editingId ? actualizarSolicitud : crearSolicitud}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <div>
              <label>Nombre adoptante</label>
              <input
                name="nombre_adoptante"
                value={form.nombre_adoptante}
                onChange={onChange}
              />
            </div>

            <div>
              <label>Correo</label>
              <input name="correo" value={form.correo} onChange={onChange} />
            </div>

            <div style={{ gridColumn: "1 / -1" }}>
              <label>Mascota (nombre)</label>
              <input
                name="mascota_nombre"
                value={form.mascota_nombre}
                onChange={onChange}
              />
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
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>
                Adoptante
              </th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>
                Correo
              </th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>
                Mascota
              </th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>
                Fecha
              </th>
              <th style={{ borderBottom: "1px solid #ccc", textAlign: "left", padding: 8 }}>
                Acciones
              </th>
            </tr>
          </thead>
          <tbody>
            {solicitudes.map((s) => (
              <tr key={s.id}>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>
                  {s.nombre_adoptante}
                </td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>{s.correo}</td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>
                  {s.mascota_nombre}
                </td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>
                  {s.fecha || "-"}
                </td>
                <td style={{ borderBottom: "1px solid #eee", padding: 8 }}>
                  <button onClick={() => startEdit(s)} style={{ marginRight: 8 }}>
                    Editar
                  </button>
                  <button onClick={() => eliminarSolicitud(s.id)}>Eliminar</button>
                </td>
              </tr>
            ))}

            {solicitudes.length === 0 && (
              <tr>
                <td colSpan={5} style={{ padding: 10 }}>
                  No hay solicitudes registradas.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
