from django.apps import apps
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST

from professions.core.models import Contact
from professions.utils.load_serializers import get_serializer_class

from .serializers import ContactModelSerializer
from .serializers import ProfessionalLookupSerializer


@extend_schema(exclude=True)
class ContactListAPIView(ListAPIView):
    queryset = Contact.objects.distinct("title")
    serializer_class = ContactModelSerializer
    permission_classes = [AllowAny]


extend_schema(exclude=True)


class ProfessionalLookupAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfessionalLookupSerializer

    def get_serializer_class(self):
        if self.request.method.lower() == "post":
            return ProfessionalLookupSerializer
        return super().get_serializer_class()

    def post(self, request: Request, *args, **kwargs):
        data = request.data.copy()
        data["model_name"] = data.pop("model")[0]
        data["professional_name"] = data.pop("name")[0]

        serializer = ProfessionalLookupSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        app_label, model_name = serializer.validated_data["model_name"].split(".")
        ModelClass = apps.get_model(app_label=app_label, model_name=model_name)

        professional_name = serializer.validated_data.get("professional_name")
        queryset = ModelClass.objects.using("cloud_readonly").filter(
            name__icontains=professional_name
        )

        serializer_class = get_serializer_class(model_name)
        if not serializer_class:
            return Response(
                {"error": "No serializer found for this model", "results": None},
                status=HTTP_400_BAD_REQUEST,
            )

        serialized = serializer_class(queryset, many=True)
        return Response({"results": serialized.data}, status=HTTP_200_OK)
