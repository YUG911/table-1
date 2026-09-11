from django.http import HttpRequest
from accounts.models import User


def current_user_context(request):
    from accounts.models import User
    uid = request.session.get('user_id')
    if uid is None:
        return {'current_user': None}
    try:
        user = User.objects.select_related('role').get(user_id=uid)
        return {'current_user': user}
    except User.DoesNotExist:
        request.session.flush()
        return {'current_user': None}


def current_user(request: HttpRequest):
    uid = request.session.get('user_id')
    if uid is None:
        return None
    try:
        return User.objects.select_related('role').get(user_id=uid)
    except User.DoesNotExist:
        request.session.flush()
        return None


def is_logged_in(request: HttpRequest) -> bool:
    return current_user(request) is not None


def role_name(request: HttpRequest) -> str:
    user = current_user(request)
    if user:
        return user.role.role_name
    return ''


def login_required(view_func):
    from functools import wraps
    from django.shortcuts import redirect
    from django.contrib import messages

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = current_user(request)
        if user is None:
            messages.error(request, "Please log in to continue.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*required_roles):
    from functools import wraps
    from django.shortcuts import redirect
    from django.contrib import messages

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = current_user(request)
            if user is None:
                messages.error(request, "Please log in to continue.")
                return redirect('login')
            user_role = user.role.role_name.lower()
            if user_role not in required_roles:
                messages.error(request, "You do not have permission to access this page.")
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def role_dashboard(user: User):
    role = user.role.role_name.lower()
    if role == 'patient':
        return 'patient_dashboard'
    elif role == 'doctor':
        return 'doctor_dashboard'
    elif role == 'clinic':
        return 'clinic_dashboard'
    elif role == 'clinic staff':
        return 'staff_dashboard'
    elif role == 'admin':
        return 'admin_dashboard'
    return 'home'
