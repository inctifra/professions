from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.professions_reader.helpers.throttle import ProjectPlanThrottle
from apps.professions_reader.mixins.apikey import APIKeyValidationMixin
from apps.professions_reader.mixins.logging import APILoggingMixin
from apps.professions_reader.mixins.queryset import DynamicQuerysetMixin
from apps.professions_reader.permissions.authentication import APIKeyAuthentication
from apps.professions_reader.permissions.permissions import HasValidAPIKey


class APIKeyReadOnlyViewSet(
    APIKeyValidationMixin,
    APILoggingMixin,
    DynamicQuerysetMixin,
    ReadOnlyModelViewSet,
):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [HasValidAPIKey]
    throttle_classes = [ProjectPlanThrottle]

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Hook after response is ready to log usage asynchronously.
        """
        self._log_success_api_entry(request, response, *args, **kwargs)
        return super().finalize_response(request, response, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
