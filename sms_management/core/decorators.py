from django.http import HttpResponseForbidden

def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.role != 'admin':
            return HttpResponseForbidden()

        return view_func(request, *args, **kwargs)

    return wrapper