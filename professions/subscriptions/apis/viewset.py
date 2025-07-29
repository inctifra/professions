# Example ViewSet (if needed)
from rest_framework import viewsets
from .models import Subscription
from .serializers import SubscriptionSerializer, WritableSubscriptionSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return WritableSubscriptionSerializer
        return SubscriptionSerializer
