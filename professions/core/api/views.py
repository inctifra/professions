from rest_framework import views
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from professions.core.models import Contact
from drf_spectacular.utils import extend_schema

from .serializers import ContactModelSerializer


@extend_schema(exclude=True)
class ContactListAPIView(ListAPIView):
    queryset = Contact.objects.distinct("title")
    serializer_class = ContactModelSerializer
    permission_classes = [AllowAny]
