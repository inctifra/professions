from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from apps.api_keys.models import APIKey
from apps.api_keys.models import APIKeySnapshot
from apps.projects.models import Domain


@login_required
@require_POST
def delete_api_key_view(request, api_key_id):
    key = get_object_or_404(APIKey, key_id=api_key_id)
    snapshot = get_object_or_404(
        APIKeySnapshot,
        uuid=key.uuid,
        user=request.user.profile,
    )
    snapshot.delete()
    key.delete()
    return JsonResponse({}, safe=False, status=204)


@login_required
@require_POST
def delete_domain_view(request, domain_id):
    domain = get_object_or_404(Domain, pk=domain_id, project__user=request.user.profile)
    related_keys_count = domain.api_keys.count()
    force_delete = request.GET.get("force") == "1"
    msg = "This domain has {} API key(s) in use. Are you sure you want to delete it?"

    if related_keys_count > 0 and not force_delete:
        return JsonResponse(
            {
                "success": False,
                "message": msg.format(related_keys_count),
                "has_keys": True,
            }
        )

    if related_keys_count > 0:
        domain.api_keys.all().delete()

    domain.delete()
    return JsonResponse(
        {
            "success": True,
            "message": "Domain and all related API keys deleted successfully.",
        }
    )
