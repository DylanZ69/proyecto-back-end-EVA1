from django.shortcuts import render, redirect

seguimientos_data = [
     {"id": 1, "mascota": "Firulais", "usuario": "usuario1", "estado": "En progreso"},
]
mascotas_data = [
    {"id": 1, "nombre": "Firulais", "edad": 3, "raza": "Mestizo", "tipo": "Perro"},
    {"id": 2, "nombre": "Pelusa", "edad": 2, "raza": "Persa", "tipo": "Gato"},
]
refugios_data = [
    {"id": 1, "nombre": "Refugio Felino", "ubicacion": "Santiago"},
    {"id": 2, "nombre": "Refugio Canino", "ubicacion": "Valparaíso"},
]

solicitudes_data = [
    {"id": 1, "usuario": "usuario1", "mascota": "Firulais", "estado": "Pendiente"},
    {"id": 2, "usuario": "usuario2", "mascota": "Pelusa", "estado": "Aprobada"},
]

USUARIOS = {
    "admin": {"password": "admin", "rol": "admin"},
    "usuario1": {"password": "abcd", "rol": "usuario"}
}

def login_view(request):
    mensaje = ""
    if request.method == "POST":
        username = request.POST.get("usuario")
        password = request.POST.get("password")
        user = USUARIOS.get(username)
        if user and user["password"] == password:
            return redirect(f'/menu/?rol={user["rol"]}')
        else:
            mensaje = "Usuario o contraseña incorrecta"
    return render(request, "templatesApp/login.html", {"mensaje": mensaje})


def menu(request):
    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/menu.html", {"rol": rol})



def index(request):
    return render(request, "templatesApp/index.html")

def mascotas(request):
    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/mascotas.html", {"mascotas": mascotas_data, "rol": rol})

def agregar_mascota(request):
    rol = request.GET.get("rol", "usuario")
    if rol != "admin":
        return redirect(f"/mascotas/?rol={rol}")

    if request.method == "POST":
        nueva_id = len(mascotas_data) + 1
        nombre = request.POST.get("nombre")
        edad = request.POST.get("edad")
        raza = request.POST.get("raza")
        tipo = request.POST.get("tipo")
        mascotas_data.append({"id": nueva_id, "nombre": nombre, "edad": edad, "raza": raza, "tipo":tipo})
        return redirect(f"/mascotas/?rol={rol}")

    return render(request, "templatesApp/agregar_mascota.html", {"rol": rol})

def eliminar_mascota(request, id):
    rol = request.GET.get("rol", "usuario")
    if rol == "admin":
        global mascotas_data
        mascotas_data = [m for m in mascotas_data if m["id"] != id]
    return redirect(f"/mascotas/?rol={rol}")

def refugios(request):
    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/refugios.html", {"refugios": refugios_data, "rol": rol})
def agregar_refugio(request):
    rol = request.GET.get("rol", "usuario")
    if rol != "admin":
        return redirect(f'/refugios/?rol={rol}')

    if request.method == "POST":
        nueva_id = len(refugios_data) + 1
        nombre = request.POST.get("nombre")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        refugios_data.append({"id": nueva_id, "nombre": nombre, "direccion": direccion, "telefono": telefono})
        return redirect(f'/refugios/?rol={rol}')

    return render(request, "templatesApp/agregar_refugios.html", {"rol": rol})

def solicitudes(request):
    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/solicitudes.html", {"solicitudes": solicitudes_data, "rol": rol})

def enviar_solicitud(request):
    rol = request.GET.get("rol", "usuario")
    if rol != "usuario":
        return redirect(f'/solicitudes/?rol={rol}')

    if request.method == "POST":
        nueva_id = len(solicitudes_data) + 1
        nombre = request.POST.get("nombre")
        mascota = request.POST.get("mascota")
        comentarios = request.POST.get("comentarios")
        solicitudes_data.append({"id": nueva_id, "nombre": nombre, "mascota": mascota, "comentarios": comentarios, "estado": "pendiente"})
        return redirect(f'/solicitudes/?rol={rol}')

    return render(request, "templatesApp/enviar_solicitud.html", {"rol": rol})

def gestionar_solicitud(request, id, accion):
    rol = request.GET.get("rol", "usuario")
    if rol != "admin":
        return redirect(f'/solicitudes/?rol={rol}')

    for solicitud in solicitudes_data:
        if solicitud["id"] == id:
            if accion == "aceptar":
                solicitud["estado"] = "aceptada"
            elif accion == "rechazar":
                solicitud["estado"] = "rechazada"
            break

    return redirect(f'/solicitudes/?rol={rol}')

def seguimientos(request):
    rol = request.GET.get("rol", "usuario")
    if rol != "admin":
        return redirect(f'/menu/?rol={rol}')
    return render(request, "templatesApp/seguimientos.html", {"seguimientos": seguimientos_data, "rol": rol})

def agregar_seguimiento(request):
    rol = request.GET.get("rol", "usuario")
    if rol != "admin":
        return redirect(f'/seguimientos/?rol={rol}')

    if request.method == "POST":
        nueva_id = len(seguimientos_data) + 1
        mascota = request.POST.get("mascota")
        usuario = request.POST.get("usuario")
        estado = request.POST.get("estado")
        seguimientos_data.append({
            "id": nueva_id,
            "mascota": mascota,
            "usuario": usuario,
            "estado": estado
        })
        return redirect(f'/seguimientos/?rol={rol}')

    return render(request, "templatesApp/agregar_seguimiento.html", {"rol": rol})