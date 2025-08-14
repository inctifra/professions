from django.http import JsonResponse

from .urls import router


def list_api_resources(request):
    """
    Returns a list of registered API resources from DRF's DefaultRouter.
    """
    resources = []
    for prefix, _, basename in router.registry:
        resources.append({
            "value": prefix,               # e.g. "advocates"
            "label": basename.title()      # e.g. "Advocates"
        })
    return JsonResponse(resources, safe=False)
