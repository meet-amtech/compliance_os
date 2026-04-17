import contextvars
from django.utils.deprecation import MiddlewareMixin

# Context variable to store the current user
_current_user = contextvars.ContextVar('current_user', default=None)

#  Context variable to store current tenant
_current_tenant = contextvars.ContextVar('current_tenant', default=None)


def get_current_user():
    """
    Retrieve the current user from the context variable.
    """
    return _current_user.get()


#  Added helper for tenant (no change to existing logic)
def get_current_tenant():
    """
    Retrieve the current tenant from the context variable.
    """
    return _current_tenant.get()


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware to extract and store the current authenticated user in thread-safe contextvars.
    """

    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            _current_user.set(request.user)

            #  Set tenant from authenticated user
            _current_tenant.set(getattr(request.user, 'tenant', None))

            # Optional but useful: attach to request object
            request.tenant = getattr(request.user, 'tenant', None)
        else:
            _current_user.set(None)
            _current_tenant.set(None)
            request.tenant = None

    def process_response(self, request, response):
        # Clear the context var to prevent leakage into another async task or thread
        _current_user.set(None)
        _current_tenant.set(None)
        return response