from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied()
                
            if request.user.is_superuser or request.user.groups.filter(name__in=allowed_roles).exists():
                return view_func(request, *args, **kwargs)
                
            raise PermissionDenied("Du hast nicht die erforderliche Rolle für diese Seite.")
        return wrapper_func
    return decorator
