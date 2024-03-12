from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse



def department_required(departments):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_department = request.user.department
                if user_department.name in departments:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, 'unauthorized.html')
            else:
                # Handle unauthenticated users
                return redirect('login')  # Redirect to login page
        return wrapped_view
    return decorator