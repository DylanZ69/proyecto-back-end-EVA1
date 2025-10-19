from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mascota, Refugio, Solicitud, Seguimiento
import json

# ----------------------------
# USUARIOS DE PRUEBA
# ----------------------------
USUARIOS = {
    "admin": {"password": "admin123", "rol": "admin"},
    "usuario": {"password": "user123", "rol": "usuario"}
}

# ----------------------------
# VISTAS BÁSICAS
# ----------------------------
def index(request):
    """Página principal HTML"""
    return render(request, "templatesApp/index.html")

def login_view(request):
    """Vista para login HTML"""
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
    """Menú principal según rol"""
    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/menu.html", {"rol": rol})

# ----------------------------
# CRUD MASCOTAS
# ----------------------------
def ver_mascotas(request):
    mascotas = Mascota.objects.all()  # <-- Importante: NO usar .values()
    rol = request.GET.get("rol", "usuario")
    return render(request, "templatesApp/mascotas.html", {"mascotas": mascotas, "rol": rol})


def obtener_mascota(request, id):
    try:
        mascota = Mascota.objects.get(pk=id)
        return JsonResponse({
            "id": mascota.id,
            "nombre": mascota.nombre,
            "especie": mascota.especie,
            "edad": mascota.edad,
            "descripcion": mascota.descripcion
        })
    except Mascota.DoesNotExist:
        return JsonResponse({"error": "Mascota no encontrada"}, status=404)

@csrf_exempt
def crear_mascota(request):
    rol = request.GET.get("rol", "usuario")  # Captura el rol desde GET
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mascota = Mascota.objects.create(
                nombre=data['nombre'],
                edad=data['edad'],
                raza=data['raza'],
                tipo=data['tipo']
            )
            return JsonResponse({"mensaje": "Mascota creada", "id": mascota.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        # Renderiza el formulario con el rol
        return render(request, "templatesApp/agregar_mascota.html", {"rol": rol})


@csrf_exempt
def actualizar_mascota(request, id):
    try:
        mascota = Mascota.objects.get(pk=id)
    except Mascota.DoesNotExist:
        return JsonResponse({"error": "Mascota no encontrada"}, status=404)

    if request.method == 'GET':
        # Renderiza un formulario HTML para editar
        rol = request.GET.get("rol", "usuario")
        return render(request, "templatesApp/actualizar_mascota.html", {"mascota": mascota, "rol": rol})

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            mascota.nombre = data.get('nombre', mascota.nombre)
            mascota.edad = data.get('edad', mascota.edad)
            mascota.raza = data.get('raza', mascota.raza)
            mascota.tipo = data.get('tipo', mascota.tipo)
            mascota.save()
            return JsonResponse({"mensaje": "Mascota actualizada"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def eliminar_mascota(request, id):
    if request.method == 'DELETE':
        try:
            mascota = Mascota.objects.get(pk=id)
            mascota.delete()
            return JsonResponse({"mensaje": "Mascota eliminada"})
        except Mascota.DoesNotExist:
            return JsonResponse({"error": "Mascota no encontrada"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

# ----------------------------
# CRUD REFUGIOS
# ----------------------------



# ----------------------------
# CRUD REFUGIOS ADAPTADO
# ----------------------------
def ver_refugios(request):
    rol = request.GET.get("rol", "usuario")
    refugios = Refugio.objects.all()
    return render(request, "templatesApp/refugios.html", {"refugios": refugios, "rol": rol})

@csrf_exempt
def crear_refugio(request):
    rol = request.GET.get("rol", "usuario")
    if request.method == "POST":
        # Tu código para guardar el refugio
        pass
    return render(request, "templatesApp/agregar_refugios.html", {"rol": rol})


@csrf_exempt
def eliminar_refugio(request, id):
    if request.method == 'DELETE':
        try:
            refugio = Refugio.objects.get(pk=id)
            refugio.delete()
            return JsonResponse({"mensaje": "Refugio eliminado"})
        except Refugio.DoesNotExist:
            return JsonResponse({"error": "Refugio no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def listar_refugios(request):
    if request.method == 'GET':
        refugios = Refugio.objects.all().values()
        return JsonResponse(list(refugios), safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def ver_refugios(request):
    rol = request.GET.get("rol", "usuario")
    refugios = Refugio.objects.all()
    return render(request, "templatesApp/refugios.html", {"refugios": refugios, "rol": rol})

@csrf_exempt
def crear_refugio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            refugio = Refugio.objects.create(
                nombre=data['nombre'],
                direccion=data['direccion'],
                telefono=data['telefono']
            )
            return JsonResponse({"mensaje": "Refugio creado", "id": refugio.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return render(request, "templatesApp/agregar_refugios.html")

@csrf_exempt
def actualizar_refugio(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            refugio = Refugio.objects.get(pk=id)
            refugio.nombre = data.get('nombre', refugio.nombre)
            refugio.direccion = data.get('direccion', refugio.direccion)
            refugio.telefono = data.get('telefono', refugio.telefono)
            refugio.save()
            return JsonResponse({"mensaje": "Refugio actualizado"})
        except Refugio.DoesNotExist:
            return JsonResponse({"error": "Refugio no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def eliminar_refugio(request, id):
    if request.method == 'DELETE':
        try:
            refugio = Refugio.objects.get(pk=id)
            refugio.delete()
            return JsonResponse({"mensaje": "Refugio eliminado"})
        except Refugio.DoesNotExist:
            return JsonResponse({"error": "Refugio no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

# ----------------------------
# CRUD SOLICITUDES DE ADOPCIÓN
# ----------------------------

# views.py
def enviar_solicitud(request):
    rol = request.GET.get("rol", "usuario")
    mascotas = Mascota.objects.all()  # Trae todas las mascotas
    return render(request, "templatesApp/enviar_solicitud.html", {"rol": rol, "mascotas": mascotas})


def ver_solicitudes(request):
    rol = request.GET.get("rol", "usuario")
    solicitudes = Solicitud.objects.all()  # Opcional: solo si quieres mostrar
    return render(request, "templatesApp/solicitudes.html", {"rol": rol, "solicitudes": solicitudes})




def listar_solicitudes(request):
    if request.method == 'GET':
        solicitudes = Solicitud.objects.all().values()
        return JsonResponse(list(solicitudes), safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)





def crear_solicitud(request):
    if request.method == "POST":
        try:
            nombre_adoptante = request.POST.get("nombre_adoptante")
            correo_adoptante = request.POST.get("correo_adoptante")
            mascota_id = request.POST.get("mascota")  # id de la mascota seleccionada
            mascota = Mascota.objects.get(pk=mascota_id)

            # Crear la solicitud
            solicitud = Solicitud.objects.create(
                nombre_adoptante=nombre_adoptante,
                correo_adoptante=correo_adoptante,
                mascota=mascota,
                estado="Pendiente"
            )

            return redirect("ver_solicitudes")  # Redirige a la lista de solicitudes

        except Exception as e:
            # Si hay error, vuelve a mostrar el form con mensaje
            return render(request, "templatesApp/enviar_solicitud.html", {
                "error": f"Error al crear la solicitud: {e}",
                "mascotas": Mascota.objects.all(),
                "rol": request.GET.get("rol", "usuario")
            })

    else:
        return redirect("enviar_solicitud")
    
@csrf_exempt
def actualizar_solicitud(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            solicitud = Solicitud.objects.get(pk=id)
            solicitud.nombre_adoptante = data.get('nombre_adoptante', solicitud.nombre_adoptante)
            solicitud.mascota_id = data.get('mascota_id', solicitud.mascota_id)
            solicitud.fecha = data.get('fecha', solicitud.fecha)
            solicitud.estado = data.get('estado', solicitud.estado)
            solicitud.save()
            return JsonResponse({"mensaje": "Solicitud actualizada"})
        except Solicitud.DoesNotExist:
            return JsonResponse({"error": "Solicitud no encontrada"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def eliminar_solicitud(request, id):
    if request.method == 'DELETE':
        try:
            solicitud = Solicitud.objects.get(pk=id)
            solicitud.delete()
            return JsonResponse({"mensaje": "Solicitud eliminada"})
        except Solicitud.DoesNotExist:
            return JsonResponse({"error": "Solicitud no encontrada"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

# ----------------------------
# CRUD SEGUIMIENTOS
# ----------------------------
def listar_seguimientos(request):
    if request.method == 'GET':
        seguimientos = Seguimiento.objects.all().values()
        return JsonResponse(list(seguimientos), safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def crear_seguimiento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seguimiento = Seguimiento.objects.create(
                solicitud_id=data['solicitud_id'],
                fecha=data['fecha'],
                observacion=data['observacion']
            )
            return JsonResponse({"mensaje": "Seguimiento creado", "id": seguimiento.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return render(request, "templatesApp/crear_seguimiento.html")

@csrf_exempt
def actualizar_seguimiento(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            seguimiento = Seguimiento.objects.get(pk=id)
            seguimiento.solicitud_id = data.get('solicitud_id', seguimiento.solicitud_id)
            seguimiento.fecha = data.get('fecha', seguimiento.fecha)
            seguimiento.observacion = data.get('observacion', seguimiento.observacion)
            seguimiento.save()
            return JsonResponse({"mensaje": "Seguimiento actualizado"})
        except Seguimiento.DoesNotExist:
            return JsonResponse({"error": "Seguimiento no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def eliminar_seguimiento(request, id):
    if request.method == 'DELETE':
        try:
            seguimiento = Seguimiento.objects.get(pk=id)
            seguimiento.delete()
            return JsonResponse({"mensaje": "Seguimiento eliminado"})
        except Seguimiento.DoesNotExist:
            return JsonResponse({"error": "Seguimiento no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)
