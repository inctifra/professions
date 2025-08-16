from django.urls import path

from professions.users.views import LoginView

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("profile/", view=user_detail_view, name="detail"),
    path("accounts/login/", LoginView.as_view(), name="account_login"),
]
