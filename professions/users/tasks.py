from celery import shared_task

from .models import User


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@shared_task
def update_user_socialapp_avatar(user_id: int, avatar_url: str):
    try:
        user = User.objects.get(id=user_id)
        user.avatar = avatar_url
        user.save(update_fields=["avatar"])
    except User.DoesNotExist:
        pass
