from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def welcome(request):
    return Response({'title': 'Welcome to RealtySellDEVELOP. Please check Documentation `https://documenter.getpostman.com/view/17461733/UzkS3HZz`'}, status=200)