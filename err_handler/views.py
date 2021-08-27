from django.core.exceptions import PermissionDenied
from django.shortcuts import render


page = 'templates/error.html'


def handler403(request, *args, **kwargs):
    response = render(request, 'errors/403.html', {})
    response.status_code = 403
    return response


def handler500(request, *args, **kwargs):
    response = render(request, 'errors/500.html', {})
    response.status_code = 500
    return response


def handler404(request, *args, **kwargs):
    response = render(request, 'errors/404.html', {})
    response.status_code = 404
    return response


def handler400(request, *args, **kwargs):
    response = render(request, 'errors/400.html', {})
    response.status_code = 400
    return response
