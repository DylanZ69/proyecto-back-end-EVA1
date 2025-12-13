from django.shortcuts import render, redirect
from django.contrib import messages
import requests

# ==========================
# CONFIGURACIÓN API
# ==========================
API_BASE_URL = "http://127.0.0.1:8001/api"


# ==========================
# VISTAS BÁSICAS
# ==========================
def index(request):
    return render(request, "templatesApp/index.html")


def menu(request):
    if "token" not in request.session:
        return redirect("login")
    return render(request, "templatesApp/menu.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")


# ==========================
# LOGIN (API TOKEN)
# ==========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = requests.post(
            f"{API_BASE_URL}/token/",
            data={"username": username, "password": password}
        )

        if response.status_code == 200:
            request.session["token"] = response.json()["token"]
            return redirect("menu")
        else:
            messages.error(request, "Credenciales incorrectas")

    return render(request, "templatesApp/login.html")


# ==========================
# HELPERS
# ==========================
def get_headers(request):
    token = request.session.get("token")
    return {"Authorization": f"Token {token}"} if token else {}


# ==========================
# MASCOTAS (API)
# ==========================
def ver_mascotas(request):
    headers = get_headers(request)
    response = requests.get(f"{API_BASE_URL}/mascotas/", headers=headers)

    mascotas = response.json() if response.status_code == 200 else []
    return render(request, "templatesApp/mascotas.html", {"mascotas": mascotas})


def crear_mascota(request):
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "edad": request.POST.get("edad"),
            "raza": request.POST.get("raza"),
            "tipo": request.POST.get("tipo"),
            "refugio_nombre": request.POST.get("refugio_nombre"),
        }

        response = requests.post(
            f"{API_BASE_URL}/mascotas/",
            headers=get_headers(request),
            data=data
        )

        if response.status_code == 201:
            messages.success(request, "Mascota creada correctamente")
            return redirect("ver_mascotas")
        else:
            messages.error(request, "Error al crear mascota")

    return render(request, "templatesApp/agregar_mascota.html")


def actualizar_mascota(request, id):
    headers = get_headers(request)

    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "edad": request.POST.get("edad"),
            "raza": request.POST.get("raza"),
            "tipo": request.POST.get("tipo"),
            "refugio_nombre": request.POST.get("refugio_nombre"),
        }

        response = requests.put(
            f"{API_BASE_URL}/mascotas/{id}/",
            headers=headers,
            data=data
        )

        if response.status_code == 200:
            messages.success(request, "Mascota actualizada")
            return redirect("ver_mascotas")
        else:
            messages.error(request, "Error al actualizar mascota")

    mascota = requests.get(
        f"{API_BASE_URL}/mascotas/{id}/",
        headers=headers
    ).json()

    return render(request, "templatesApp/actualizar_mascota.html", {"mascota": mascota})


def eliminar_mascota(request, id):
    if request.method == "POST":
        requests.delete(
            f"{API_BASE_URL}/mascotas/{id}/",
            headers=get_headers(request)
        )
        messages.success(request, "Mascota eliminada")
        return redirect("ver_mascotas")

    mascota = requests.get(
        f"{API_BASE_URL}/mascotas/{id}/",
        headers=get_headers(request)
    ).json()

    return render(request, "templatesApp/confirmar_eliminar_mascota.html", {"mascota": mascota})


# ==========================
# REFUGIOS (API)
# ==========================
def ver_refugios(request):
    response = requests.get(
        f"{API_BASE_URL}/refugios/",
        headers=get_headers(request)
    )
    refugios = response.json() if response.status_code == 200 else []
    return render(request, "templatesApp/refugios.html", {"refugios": refugios})


def crear_refugio(request):
    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "direccion": request.POST.get("direccion"),
            "telefono": request.POST.get("telefono"),
        }

        response = requests.post(
            f"{API_BASE_URL}/refugios/",
            headers=get_headers(request),
            data=data
        )

        if response.status_code == 201:
            messages.success(request, "Refugio creado")
            return redirect("ver_refugios")
        else:
            messages.error(request, "Error al crear refugio")

    return render(request, "templatesApp/agregar_refugios.html")

def actualizar_refugio(request, id):
    headers = get_headers(request)

    if request.method == "POST":
        data = {
            "nombre": request.POST.get("nombre"),
            "direccion": request.POST.get("direccion"),
            "telefono": request.POST.get("telefono"),
        }

        response = requests.put(
            f"{API_BASE_URL}/refugios/{id}/",
            headers=headers,
            data=data
        )

        if response.status_code in (200, 204):
            messages.success(request, "Refugio actualizado")
            return redirect("ver_refugios")
        else:
            messages.error(request, "Error al actualizar refugio")

    refugio = requests.get(
        f"{API_BASE_URL}/refugios/{id}/",
        headers=headers
    ).json()

    return render(request, "templatesApp/actualizar_refugio.html", {"refugio": refugio})


def eliminar_refugio(request, id):
    if request.method == "POST":
        requests.delete(
            f"{API_BASE_URL}/refugios/{id}/",
            headers=get_headers(request)
        )
        messages.success(request, "Refugio eliminado")
        return redirect("ver_refugios")

    refugio = requests.get(
        f"{API_BASE_URL}/refugios/{id}/",
        headers=get_headers(request)
    ).json()

    return render(
        request,
        "templatesApp/confirmar_eliminar_refugio.html",
        {"refugio": refugio}
    )

# ==========================
# SOLICITUDES (API)
# ==========================
def ver_solicitudes(request):
    response = requests.get(
        f"{API_BASE_URL}/solicitudes/",
        headers=get_headers(request)
    )
    solicitudes = response.json() if response.status_code == 200 else []
    return render(request, "templatesApp/solicitudes.html", {"solicitudes": solicitudes})


def crear_solicitud(request):
    if request.method == "POST":
        data = {
            "nombre_adoptante": request.POST.get("nombre_adoptante"),
            "correo": request.POST.get("correo"),
            "mascota_nombre": request.POST.get("mascota_nombre"),
        }

        response = requests.post(
            f"{API_BASE_URL}/solicitudes/",
            headers=get_headers(request),
            data=data
        )

        if response.status_code == 201:
            messages.success(request, "Solicitud enviada")
            return redirect("ver_solicitudes")
        else:
            messages.error(request, "Error al enviar solicitud")

    return render(request, "templatesApp/enviar_solicitud.html")
def actualizar_solicitud(request, id):
    headers = get_headers(request)

    if request.method == "POST":
        data = {
            "nombre_adoptante": request.POST.get("nombre_adoptante"),
            "correo": request.POST.get("correo"),
            "mascota_nombre": request.POST.get("mascota_nombre"),
        }

        response = requests.put(
            f"{API_BASE_URL}/solicitudes/{id}/",
            headers=headers,
            data=data
        )

        if response.status_code in (200, 204):
            messages.success(request, "Solicitud actualizada")
            return redirect("ver_solicitudes")
        else:
            messages.error(request, "Error al actualizar solicitud")

    solicitud = requests.get(
        f"{API_BASE_URL}/solicitudes/{id}/",
        headers=headers
    ).json()

    return render(
        request,
        "templatesApp/actualizar_solicitud.html",
        {"solicitud": solicitud}
    )


def eliminar_solicitud(request, id):
    if request.method == "POST":
        requests.delete(
            f"{API_BASE_URL}/solicitudes/{id}/",
            headers=get_headers(request)
        )
        messages.success(request, "Solicitud eliminada")
        return redirect("ver_solicitudes")

    solicitud = requests.get(
        f"{API_BASE_URL}/solicitudes/{id}/",
        headers=get_headers(request)
    ).json()

    return render(
        request,
        "templatesApp/confirmar_eliminar_solicitud.html",
        {"solicitud": solicitud}
    )
