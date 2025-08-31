from django.shortcuts import render


def handler_403_view(request, exception=None):
    return render(request, "403.html", status=403)


def handler_404_view(request, exception=None):
    return render(request, "404.html", status=404)


def handler_500_view(request):
    return render(request, "500.html", status=500)


def handler_503_view(request, exception=None):
    return render(request, "503.html", status=503)
