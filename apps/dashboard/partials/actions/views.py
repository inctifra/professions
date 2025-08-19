from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from apps.api_keys.models import APIKey
from apps.api_keys.models import APIKeySnapshot


@login_required
@require_POST
def delete_api_key_view(request, api_key_id):
    key = get_object_or_404(APIKey, key_id=api_key_id)
    snapshot = get_object_or_404(
        APIKeySnapshot, uuid=key.uuid, user=request.user.profile
    )
    snapshot.delete()
    key.delete()
    return JsonResponse({}, safe=False, status=204)
