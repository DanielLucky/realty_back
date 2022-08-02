import django_filters
from django_filters import rest_framework
from rest_framework import generics, permissions, filters
from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser, FormParser

from .models import Realty, City
from .permissions import IsOwnerOrReadOnly
from .serializers import RealtySerializer, RealtyCRUDSerializer, RealtyCitySerializer
from .services import PaginationRealtyList


class RegistrationManagerFilter(rest_framework.FilterSet):
    city = rest_framework.NumberFilter(field_name='address__city__id')
    type = rest_framework.CharFilter(field_name='realty_type')
    format = rest_framework.CharFilter(field_name='realty_format')
    price = rest_framework.NumberFilter(field_name='price', lookup_expr='gte')

    class Meta:
        model = Realty
        fields = '__all__'


class RealtyAPIView(generics.ListAPIView):
    queryset = Realty.objects.all().filter(is_banned=False, is_visible=True)
    serializer_class = RealtySerializer
    pagination_class = PaginationRealtyList
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = RegistrationManagerFilter


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


class RealtyCity(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = RealtyCitySerializer

