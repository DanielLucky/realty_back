from django.urls import path, include

from realty.views import RealtyAPIView, RealtyAdd, RealtyCRUD


urlpatterns = [
    path('realty/', RealtyAPIView.as_view()),
    path('realty/add', RealtyAdd.as_view()),
    path('realty/<int:pk>', RealtyCRUD.as_view())
]