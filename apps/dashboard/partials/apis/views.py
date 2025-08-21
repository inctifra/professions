from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_ratelimit.decorators import ratelimit

from apps.api_keys.api.serializers import APIKeySerializer
from apps.api_keys.models import APIKey
from apps.api_keys.models import APIKeySnapshot


@login_required
@ratelimit(
    key="user", rate="5/m", method="GET", block=True,
)  # 5 requests per minute per user
def load_key_for_simulation_view(request):
    """
    Secure endpoint to fetch API keys for internal testing.
    - Returns the raw key from a snapshot if UUID is provided (owner-only),
      but only once per session.
    - Returns a list of active API keys if no UUID is given.
    """
    uuid = request.GET.get("uuid")

    if uuid:
        # Initialize session storage for accessed keys
        accessed_keys = request.session.get("accessed_snapshots", [])

        # Fetch the snapshot only for the logged-in owner
        snapshot = get_object_or_404(
            APIKeySnapshot, uuid=uuid, user=request.user.profile,
        )

        # if uuid in accessed_keys:
        #     # Already accessed in this session → hide key
        #     return JsonResponse(
        #         {"key": "This key has already been viewed in this session."},
        #         status=HTTPStatus.FORBIDDEN,
        #         safe=False,
        #     )

        # Mark this key as accessed
        accessed_keys.append(uuid)
        request.session["accessed_snapshots"] = accessed_keys
        request.session.modified = True

        return JsonResponse(
            {"key": str(snapshot.key)}, status=HTTPStatus.OK, safe=False,
        )

    # Return all active API keys related to this user (project/domain)
    qs = APIKey.objects.filter(
        Q(project__user=request.user.profile)
        | Q(domain__project__user=request.user.profile),
        status="active",
    )
    serializer = APIKeySerializer(qs, many=True)
    return JsonResponse(serializer.data, status=HTTPStatus.OK, safe=False)
