from django.urls import path

from welcome.views import welcome

urlpatterns = [
    path('', welcome),

]
