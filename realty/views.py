from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import generics, serializers, status, permissions
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Realty, RealtyImage
from .permissions import IsOwnerOrReadOnly
from .serializers import RealtySerializer, RealtyCRUDSerializer


class Logout(APIView):
    def get(self):
        self.request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class RealtyAPIView(generics.ListAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtySerializer


class RealtyAdd(generics.CreateAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtyCRUDSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class RealtyCRUD(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtyCRUDSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


