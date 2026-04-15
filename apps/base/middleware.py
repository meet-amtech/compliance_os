import contextvars
from django.utils.deprecation import MiddlewareMixin

# Context variable to store the current user
_current_user = contextvars.ContextVar('current_user', default=None)

def get_current_user():
    """
    Retrieve the current user from the context variable.
    """
    return _current_user.get()

class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware to extract and store the current authenticated user in thread-safe contextvars.
    """
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            _current_user.set(request.user)
        else:
            _current_user.set(None)
            
    def process_response(self, request, response):
        # Clear the context var to prevent leakage into another async task or thread
        _current_user.set(None)
        return response
