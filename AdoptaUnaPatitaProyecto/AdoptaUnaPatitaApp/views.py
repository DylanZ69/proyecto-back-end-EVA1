from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mascota, Refugio, Solicitud, Seguimiento, Usuario
from .forms import UsuarioForm
from .decorators import admin_required
from .forms import MascotaForm 
from .forms import SolicitudForm
import json
from .forms import RefugioForm



# ----------------------------
# VISTAS BÁSICAS
# ----------------------------
def index(request):
    """Página principal HTML"""
    return render(request, "templatesApp/index.html")

def registrar_usuario(request):
    mensaje = ""
    if request.method == "POST":
        form = UsuarioForm(request.POST) 
        if form.is_valid():
            rol_form = form.cleaned_data['rol']

            # Verificar si hay al menos un admin en la DB
            existe_admin = Usuario.objects.filter(rol='admin').exists()

            if rol_form == 'admin' and existe_admin and request.session.get('rol') != 'admin':
                mensaje = "No tienes permisos para crear un administrador"
            else:
                usuario = form.save(commit=False)
                usuario.set_password(form.cleaned_data['password'])
                usuario.save()
                return redirect('login')
        else:
            mensaje = "Formulario no válido"
    else:
        form = UsuarioForm()

    return render(request, "templatesApp/registro.html", {"form": form, "mensaje": mensaje})


def login_view(request):
    mensaje = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(username=username)
            if usuario.check_password(password):
                # Guardar datos de sesión
                request.session['username'] = usuario.username
                request.session['rol'] = usuario.rol

                # Redirigir según el rol
                if usuario.rol == 'admin':
                    return redirect('menu')  
                else:
                    return redirect('menu')  
            else:
                mensaje = "Contraseña incorrecta"
        except Usuario.DoesNotExist:
            mensaje = "Usuario no encontrado"

    return render(request, "templatesApp/login.html", {"mensaje": mensaje})

def logout_view(request):
    request.session.flush()  # elimina toda la sesión
    return redirect('login')


def menu(request):
    """Menú principal según rol guardado en sesión"""
    rol = request.session.get("rol", "usuario")
    return render(request, "templatesApp/menu.html", {"rol": rol})


# ----------------------------
# CRUD MASCOTAS
# ----------------------------
def ver_mascotas(request):
    mascotas = Mascota.objects.all() 
    rol = request.session.get("rol", "usuario")
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
@admin_required

def crear_mascota(request):
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        data = json.loads(request.body)
        form = MascotaForm(data)

        if form.is_valid():
            mascota = form.save()
            return JsonResponse({"mensaje": "Mascota creada", "id": mascota.id}, status=201)

        else:
            error_texto = list(form.errors.values())[0][0]
            return JsonResponse({"error": error_texto}, status=400)

    return render(request, "templatesApp/agregar_mascota.html", {"rol": rol})

@csrf_exempt
@admin_required
def actualizar_mascota(request, id):
    try:
        mascota = Mascota.objects.get(pk=id)
    except Mascota.DoesNotExist:
        return JsonResponse({"error": "Mascota no encontrada"}, status=404)

    if request.method == 'GET':
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
@admin_required
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

def ver_refugios(request):
    rol = request.session.get("rol", "usuario")
    refugios = Refugio.objects.all()
    return render(request, "templatesApp/refugios.html", {"refugios": refugios, "rol": rol})

@csrf_exempt
@admin_required
def crear_refugio(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = RefugioForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse({"mensaje": "Refugio creado"}, status=201)

        else:
            error_texto = list(form.errors.values())[0][0]
            return JsonResponse({"error": error_texto}, status=400)

    return render(request, "templatesApp/agregar_refugios.html")

@csrf_exempt
def listar_refugios(request):
    if request.method == 'GET':
        refugios = Refugio.objects.all().values()
        return JsonResponse(list(refugios), safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
@admin_required
def actualizar_refugio(request, id):
    try:
        refugio = Refugio.objects.get(pk=id)
    except Refugio.DoesNotExist:
        return JsonResponse({"error": "Refugio no encontrado"}, status=404)

    if request.method == 'GET':
        rol = request.session.get("rol", "usuario")
        return render(request, "templatesApp/actualizar_refugio.html", {"refugio": refugio, "rol": rol})

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            refugio.nombre = data.get('nombre', refugio.nombre)
            refugio.direccion = data.get('direccion', refugio.direccion)
            refugio.telefono = data.get('telefono', refugio.telefono)
            refugio.save()
            return JsonResponse({"mensaje": "Refugio actualizado"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
@admin_required
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

def enviar_solicitud(request):
    rol = request.session.get("rol", "usuario")
    mascotas = Mascota.objects.all() 
    return render(request, "templatesApp/enviar_solicitud.html", {"rol": rol, "mascotas": mascotas})


def ver_solicitudes(request):
    rol = request.session.get("rol", "usuario")
    solicitudes = Solicitud.objects.all()
    return render(request, "templatesApp/solicitudes.html", {"rol": rol, "solicitudes": solicitudes})




def listar_solicitudes(request):
    if request.method == 'GET':
        solicitudes = Solicitud.objects.all().values()
        return JsonResponse(list(solicitudes), safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def crear_solicitud(request):
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/solicitudes/?rol={rol}")
        else:
            mascotas = Mascota.objects.all()
            return render(request, "templatesApp/enviar_solicitud.html", {
                "error": form.errors,
                "mascotas": mascotas,
                "rol": rol
            })

    return redirect(f"/enviar_solicitud/?rol={rol}")



@csrf_exempt
@admin_required
def actualizar_solicitud(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            solicitud = Solicitud.objects.get(pk=id)
            solicitud.nombre_adoptante = data.get('nombre_adoptante', solicitud.nombre_adoptante)
            solicitud.comentarios = data.get('comentarios', solicitud.comentarios)
            solicitud.estado = data.get('estado', solicitud.estado)

            if 'mascota_id' in data:
                mascota = Mascota.objects.get(pk=data['mascota_id'])
                solicitud.mascota_id = mascota.id
                solicitud.mascota_nombre = mascota.nombre

            solicitud.save()
            return JsonResponse({"mensaje": "Solicitud actualizada"})
        except Solicitud.DoesNotExist:
            return JsonResponse({"error": "Solicitud no encontrada"}, status=404)
        except Mascota.DoesNotExist:
            return JsonResponse({"error": "Mascota no encontrada"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
@admin_required
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
@admin_required
def crear_seguimiento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mascota = Mascota.objects.get(pk=data['mascota_id'])
            seguimiento = Seguimiento.objects.create(
                mascota_id=mascota.id,
                mascota_nombre=mascota.nombre,
                usuario=data['usuario'],
                estado=data['estado']
            )
            return JsonResponse({"mensaje": "Seguimiento creado", "id": seguimiento.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@admin_required
def actualizar_seguimiento(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            seguimiento = Seguimiento.objects.get(pk=id)
            seguimiento.mascota_id = data.get('mascota_id', seguimiento.mascota_id)
            seguimiento.mascota_nombre = data.get('mascota_nombre', seguimiento.mascota_nombre)
            seguimiento.usuario = data.get('usuario', seguimiento.usuario)
            seguimiento.estado = data.get('estado', seguimiento.estado)
            seguimiento.save()
            return JsonResponse({"mensaje": "Seguimiento actualizado"})
        except Seguimiento.DoesNotExist:
            return JsonResponse({"error": "Seguimiento no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
@admin_required
def eliminar_seguimiento(request, id):
    if request.method == 'DELETE':
        try:
            seguimiento = Seguimiento.objects.get(pk=id)
            seguimiento.delete()
            return JsonResponse({"mensaje": "Seguimiento eliminado"})
        except Seguimiento.DoesNotExist:
            return JsonResponse({"error": "Seguimiento no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)
