from django.urls import path

from profiles.views import ProfileGetPost

urlpatterns = [
    path('me/', ProfileGetPost.as_view())
]
