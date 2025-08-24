from django.http import JsonResponse

from apps.professions_reader.versions.urls import router_v1


def list_api_resources(request):
    """
    Returns a list of registered API resources with schema metadata
    (filters, search fields, ordering fields) from DRF's DefaultRouter.
    """
    resources = []
    for prefix, viewset, basename in router_v1.registry:
        resource = {
            "value": prefix,
            "label": basename.title(),
            "schema": {},
        }

        # Extract schema-like metadata from the ViewSet
        resource["schema"]["filterset_fields"] = getattr(
            viewset, "filterset_fields", []
        )
        resource["schema"]["search_fields"] = getattr(viewset, "search_fields", [])
        resource["schema"]["ordering_fields"] = getattr(viewset, "ordering_fields", [])

        resources.append(resource)

    return JsonResponse(resources, safe=False)
