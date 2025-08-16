from celery import shared_task
from django.shortcuts import get_object_or_404

from professions.users.models import Profile
from .models import APIKey, APIKeySnapshot


@shared_task
def create_apikey_snapshot(api_key_uuid, user_id, key):
    """
    Celery task to create a snapshot of an APIKey.
    """
    user = get_object_or_404(Profile, id=user_id)
    api_key = get_object_or_404(APIKey, uuid=api_key_uuid)

    snapshot = APIKeySnapshot(user=user, uuid=api_key.uuid, key=key)
    snapshot.save()

    return str(snapshot.uuid)
