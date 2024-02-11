from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets

from agent.api.serializers import BusinessSerializer
from agent.models import Business


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.all()
