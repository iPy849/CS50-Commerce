#Built-in imports
from functools import wraps

#Django imports
from django.shortcuts import redirect

def authentication_required(f):
    @wraps(f)
    def wrapper(request):
        if request.user.is_authenticated:
            return f(request)
        else:
            return redirect('login')

    return wrapper