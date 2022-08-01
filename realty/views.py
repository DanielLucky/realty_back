from rest_framework import generics, permissions

from .models import Realty
from .permissions import IsOwnerOrReadOnly
from .serializers import RealtySerializer, RealtyCRUDSerializer, RealtyNewSerializer
from .services import PaginationRealtyList


class RealtyAPIView(generics.ListAPIView):
    queryset = Realty.objects.all().filter(is_banned=False, is_visible=True)
    serializer_class = RealtySerializer
    pagination_class = PaginationRealtyList


class RealtyUser(generics.ListAPIView):
    serializer_class = RealtySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = PaginationRealtyList

    def get_queryset(self):
        user = self.request.user
        return Realty.objects.all().filter(user=user)


class RealtyAdd(generics.CreateAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtyCRUDSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class RealtyCRUD(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtyCRUDSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class RealtyNew(generics.RetrieveUpdateAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtyNewSerializer
