from django.http import JsonResponse

from professions.professions_reader.versions.urls import router_v1


def list_api_resources(request):
    """
    Returns a list of registered API resources from DRF's DefaultRouter.
    """
    resources = []
    for prefix, _, basename in router_v1.registry:
        resources.append(
            {
                "value": prefix,  # e.g. "advocates"
                "label": basename.title(),  # e.g. "Advocates"
            }
        )
    return JsonResponse(resources, safe=False)
