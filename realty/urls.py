from django.urls import path, include

from realty.views import RealtyAPIView, RealtyAdd, RealtyCRUD, RealtyUser, RealtyNew

urlpatterns = [
    path('realty/', RealtyAPIView.as_view()),
    path('realtyNew/<int:pk>', RealtyNew.as_view()),
    path('realty/me', RealtyUser.as_view()),
    path('realty/add', RealtyAdd.as_view()),
    path('realty/<int:pk>', RealtyCRUD.as_view())
]
