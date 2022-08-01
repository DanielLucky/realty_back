
from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializerGetPost(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


