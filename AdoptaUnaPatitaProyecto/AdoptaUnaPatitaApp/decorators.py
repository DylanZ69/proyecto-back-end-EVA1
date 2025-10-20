from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        rol = request.session.get('rol')
        if rol != 'admin':
            return redirect('menu')  # redirige al menú si no es admin
        return view_func(request, *args, **kwargs)
    return wrapper
