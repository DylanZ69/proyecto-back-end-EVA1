from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mascota, Refugio, Solicitud, Usuario
from .forms import UsuarioForm
from .decorators import admin_required
from .forms import MascotaForm 
from .forms import SolicitudForm
import json
from .forms import RefugioForm
from .forms import SolicitudPublicForm



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
# CRUD MASCOTAS (HTML REAL)
# ----------------------------

def ver_mascotas(request):
    """Listado de mascotas"""
    rol = request.session.get("rol", "usuario")
    mascotas = Mascota.objects.all()
    return render(request, "templatesApp/mascotas.html", {
        "mascotas": mascotas,
        "rol": rol
    })


def obtener_mascota(request, id):
    """Detalle de una mascota"""
    mascota = get_object_or_404(Mascota, pk=id)
    rol = request.session.get("rol", "usuario")
    return render(request, "templatesApp/detalle_mascota.html", {
        "mascota": mascota,
        "rol": rol
    })


@admin_required
def crear_mascota(request):
    """Crear nueva mascota (solo admin)"""
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mascota creada correctamente.")
            return redirect("listar_mascotas")
        else:
            messages.error(request, "Hay errores en el formulario. Revisa los campos.")
    else:
        form = MascotaForm()

    return render(request, "templatesApp/agregar_mascota.html", {
        "form": form,
        "rol": rol
    })


@admin_required
def actualizar_mascota(request, id):
    """Actualizar una mascota existente (solo admin)"""
    mascota = get_object_or_404(Mascota, pk=id)
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, "Mascota actualizada correctamente.")
            return redirect("listar_mascotas")
        else:
            messages.error(request, "Hay errores en el formulario. Corrígelos.")
    else:
        form = MascotaForm(instance=mascota)

    return render(request, "templatesApp/actualizar_mascota.html", {
        "form": form,
        "mascota": mascota,
        "rol": rol
    })


@admin_required
def eliminar_mascota(request, id):
    """Eliminar una mascota (con confirmación y solo admin)"""
    mascota = get_object_or_404(Mascota, pk=id)
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        mascota.delete()
        messages.success(request, "Mascota eliminada correctamente.")
        return redirect("listar_mascotas")

    # GET: mostrar pantalla de confirmación
    return render(request, "templatesApp/confirmar_eliminar_mascota.html", {
        "mascota": mascota,
        "rol": rol
    })


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
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        form = RefugioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Refugio agregado correctamente")
            return redirect("ver_refugios")
    else:
        form = RefugioForm()

    return render(request, "templatesApp/agregar_refugios.html", {
        "form": form,
        "rol": rol
    })


@csrf_exempt
def listar_refugios(request):
    if request.method == 'GET':
        refugios = Refugio.objects.all().values()
        return JsonResponse(list(refugios), safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
@admin_required
def actualizar_refugio(request, id):
    refugio = get_object_or_404(Refugio, pk=id)
    rol = request.session.get("rol", "usuario")

    if request.method == "POST":
        form = RefugioForm(request.POST, instance=refugio)
        if form.is_valid():
            form.save()
            messages.success(request, "Refugio actualizado correctamente.")
            return redirect("ver_refugios")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        # 👇 ESTA LÍNEA precarga los datos en el form
        form = RefugioForm(instance=refugio)

    return render(request, "templatesApp/actualizar_refugio.html", {
        "form": form,
        "refugio": refugio,
        "rol": rol
    })



@csrf_exempt
@admin_required
def eliminar_refugio(request, id):
    refugio = get_object_or_404(Refugio, pk=id)

    if request.method == "POST":
        refugio.delete()
        messages.success(request, "Refugio eliminado correctamente.")
        return redirect("ver_refugios")

    return render(request, "templatesApp/confirmar_eliminar_refugio.html", {
        "refugio": refugio,
        "rol": request.session.get("rol", "usuario")
    })




def detalle_refugio(request, id):
    refugio = get_object_or_404(Refugio, pk=id)
    rol = request.session.get("rol", "usuario")
    return render(request, "templatesApp/detalle_refugio.html", {
        "refugio": refugio,
        "rol": rol
    })




# ==============================
# CRUD SOLICITUDES (HTML REAL)
# ==============================

from django.contrib import messages

def ver_solicitudes(request):
    rol = request.session.get("rol", "usuario")
    solicitudes = Solicitud.objects.all().order_by('-fecha')
    return render(request, "templatesApp/solicitudes.html", {
        "solicitudes": solicitudes,
        "rol": rol
    })


def detalle_solicitud(request, id):
    rol = request.session.get("rol", "usuario")
    solicitud = get_object_or_404(Solicitud, pk=id)
    return render(request, "templatesApp/detalle_solicitud.html", {
        "solicitud": solicitud,
        "rol": rol
    })


def enviar_solicitud(request):
    rol = request.session.get("rol", "usuario")
    mascotas = Mascota.objects.all()

    if request.method == "POST":
        form = SolicitudForm(request.POST)
        if form.is_valid():

            mascota = form.cleaned_data['mascota_fk']

            Solicitud.objects.create(
                nombre_adoptante=form.cleaned_data['nombre_adoptante'],
                correo_adoptante=form.cleaned_data['correo_adoptante'],

                mascota_fk=mascota,
                mascota_id=mascota.id,
                mascota_nombre=mascota.nombre
            )

            messages.success(request, "Solicitud enviada correctamente.")
            return redirect("ver_solicitudes")   # ← FIX

        else:
            messages.error(request, "Revisa los errores del formulario.")
            return render(request, "templatesApp/enviar_solicitud.html", {
                "form": form,
                "mascotas": mascotas,
                "rol": rol
            })

    form = SolicitudForm()
    return render(request, "templatesApp/enviar_solicitud.html", {
        "form": form,
        "mascotas": mascotas,
        "rol": rol
    })





@admin_required
def actualizar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, pk=id)
    rol = request.session.get("rol", "usuario")
    mascotas = Mascota.objects.all()

    if request.method == "POST":
        form = SolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            mascota = form.cleaned_data['mascota_fk']

            solicitud.nombre_adoptante = form.cleaned_data['nombre_adoptante']
            solicitud.correo_adoptante = form.cleaned_data['correo_adoptante']
            solicitud.mascota_fk = mascota
            solicitud.mascota_id = mascota.id
            solicitud.mascota_nombre = mascota.nombre

            solicitud.save()

            messages.success(request, "Solicitud actualizada correctamente.")
            return redirect("ver_solicitudes")  # ← CORRECTO

        else:
            messages.error(request, "Corrige los errores del formulario.")

    else:
        form = SolicitudForm(instance=solicitud)

    return render(request, "templatesApp/actualizar_solicitud.html", {
        "form": form,
        "solicitud": solicitud,
        "mascotas": mascotas,
        "rol": rol
    })




@admin_required
def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, pk=id)

    if request.method == "POST":
        solicitud.delete()
        messages.success(request, "Solicitud eliminada correctamente.")
        return redirect("ver_solicitudes")

    return render(request, "templatesApp/confirmar_eliminar_solicitud.html", {
        "solicitud": solicitud,
        "rol": request.session.get("rol", "usuario")
    })




