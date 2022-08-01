from rest_framework import generics, status
from rest_framework.response import Response

from profiles.models import Profile
from profiles.serializers import ProfileSerializerGetPost
from rest_framework.views import APIView
from rest_framework import permissions


class ProfileGetPost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, **kwargs):
        profile_obj = Profile.objects.get(user=request.user)
        data = ProfileSerializerGetPost(profile_obj).data
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):
        ProfileSerializerGetPost(data=request.data)
        profile_obj = Profile.objects.get(user=request.user)
        data_req = {
            'name': request.data.get('name', profile_obj.name),
            'surname': request.data.get('surname', profile_obj.surname),
            'description': request.data.get('description', profile_obj.description),
            'phone': request.data.get('phone', profile_obj.phone),
            'phone_verified': request.data.get('phone_verified', profile_obj.phone_verified),
            'image': request.FILES.get('image', profile_obj.image)
        }
        profile_serialize = ProfileSerializerGetPost(data=data_req)
        if profile_serialize.is_valid():
            profile_obj.name = data_req.get('name')
            profile_obj.surname = data_req.get('surname')
            profile_obj.description = data_req.get('description')
            profile_obj.phone = data_req.get('phone')
            profile_obj.phone_verified = data_req.get('phone_verified')
            profile_obj.image = data_req.get('image')
            profile_obj.save()

            return Response(data=ProfileSerializerGetPost(profile_obj).data)
        return Response(profile_serialize.errors, status=status.HTTP_400_BAD_REQUEST)



