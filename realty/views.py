from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import generics, serializers
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Realty, RealtyImage
from .serializers import RealtySerializer, RealtyCRUDSerializer


class RealtyAPIView(generics.ListAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtySerializer


class RealtyAdd(generics.CreateAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtyCRUDSerializer


class RealtyCRUD(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Realty.objects.all()
    serializer_class = RealtyCRUDSerializer

