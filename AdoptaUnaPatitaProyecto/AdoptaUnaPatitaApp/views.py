from django.shortcuts import render, redirect

# datos simulados para la app, simulando una base de datos
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

# diccionario de usuarios con contraseña y rol
USUARIOS = {
    "admin": {"password": "admin", "rol": "admin"},
    "usuario1": {"password": "abcd", "rol": "usuario"}
}

# vistas de la app

def login_view(request):
    
    """
    Vista para manejar el login de usuarios.
    - Si es POST, valida usuario y contraseña.
    - Redirige a menu según el rol.
    - Si falla, muestra mensaje de error.
    """
    
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

    """
    Vista del menú principal.
    - Recibe el rol por GET para personalizar opciones.
    """
    
    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/menu.html", {"rol": rol})



def index(request):

    """
    Vista de la página principal o index.
    """ 

    return render(request, "templatesApp/index.html")

def mascotas(request):

    """
    Vista para mostrar todas las mascotas.
    - Pasa la lista de mascotas y el rol del usuario al template.
    """

    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/mascotas.html", {"mascotas": mascotas_data, "rol": rol})

def agregar_mascota(request):

    """
    Vista para agregar una nueva mascota (solo admin).
    - Si no es admin, redirige a la lista de mascotas.
    - Si es POST, toma datos del formulario y agrega la mascota.
    """

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

    """
    Vista para eliminar una mascota (solo admin).
    - Filtra la lista de mascotas excluyendo la que coincide con el ID.
    """

    rol = request.GET.get("rol", "usuario")
    if rol == "admin":
        global mascotas_data
        mascotas_data = [m for m in mascotas_data if m["id"] != id]
    return redirect(f"/mascotas/?rol={rol}")

def refugios(request):

    """
    Vista para mostrar todos los refugios.
    """

    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/refugios.html", {"refugios": refugios_data, "rol": rol})

def agregar_refugio(request):

    """
    Vista para agregar un refugio (solo admin).
    - Si es POST, agrega un nuevo refugio con los datos del formulario.
    """

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

    """
    Vista para mostrar todas las solicitudes de adopción.
    """

    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/solicitudes.html", {"solicitudes": solicitudes_data, "rol": rol})

def enviar_solicitud(request):

    """
    Vista para que un usuario envíe una nueva solicitud de adopción.
    - Solo usuarios pueden enviar solicitudes.
    - Si es POST, agrega la solicitud a la lista.
    """

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

    """
    Vista para que el admin gestione solicitudes (aceptar/rechazar).
    - Cambia el estado de la solicitud según la acción.
    """

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

    """
    Vista para que el admin vea todos los seguimientos.
    - Solo accesible para admin.
    """

    rol = request.GET.get("rol", "usuario")
    if rol != "admin":
        return redirect(f'/menu/?rol={rol}')
    return render(request, "templatesApp/seguimientos.html", {"seguimientos": seguimientos_data, "rol": rol})

