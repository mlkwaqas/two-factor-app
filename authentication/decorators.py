from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect, resolve_url


def user_is_entry_author(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    def wrap(request, *args, **kwargs):
        user = request.user
        path = request.build_absolute_uri()
        resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
        if user.is_authenticated() and user.profile.authy_status == 'approved':
            return function(request, *args, **kwargs)
        else:
            return redirect_to_login(path, resolved_login_url, redirect_field_name)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap