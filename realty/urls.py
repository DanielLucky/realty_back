from django.urls import path, include

from realty.serializers import realty_search
from realty.views import RealtyAPIView, RealtyAdd, RealtyCRUD, RealtyUser, RealtyCity

urlpatterns = [
    path('realty/', RealtyAPIView.as_view()),
    path('realty/me', RealtyUser.as_view()),
    path('realty/search', realty_search),
    path('realty/add', RealtyAdd.as_view()),
    path('realty/<int:pk>', RealtyCRUD.as_view()),
    path('city/', RealtyCity.as_view()),
]
