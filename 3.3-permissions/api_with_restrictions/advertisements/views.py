from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsCreatorOrAdmin
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            queryset = Advertisement.objects.filter(
                status__in=['OPEN', 'CLOSED']
            )
        else:
            queryset = Advertisement.objects.exclude(
                status='DRAFT', creator__lt=user
            ).exclude(
                status='DRAFT', creator__gt=user
            )
        return queryset

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsCreatorOrAdmin()]
        return []
