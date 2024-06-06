from functools import wraps

from django.http import Http404


def create_decorator(test_func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            raise Http404
        return _wrapped_view
    return decorator


def blogger_required(function=None):
    decorator = create_decorator(lambda u: u.is_active and u.is_blogger)
    if function:
        return decorator(function)
    return decorator


def musician_required(function=None):
    decorator = create_decorator(lambda u: u.is_active and u.is_musician)
    if function:
        return decorator(function)
    return decorator
