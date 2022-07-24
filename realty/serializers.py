import PIL
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from PIL import Image
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from realty_back import settings
from .models import *


class ImageUrlField(serializers.ModelSerializer):

    class Meta:
        model = RealtyImage
        fields = ['image', 'created_at']

    def to_representation(self, instance):
        url = 'http://127.0.0.1:8000'+settings.MEDIA_URL+instance.image.name  # TODO: Изменить на проде

        return url


class RealtySerializer(serializers.ModelSerializer):
    image = ImageUrlField(many=True, read_only=True)
    city = serializers.CharField(source='address.city.title')
    street = serializers.CharField(source='address.street.title')
    house = serializers.CharField(source='address.house.title', allow_blank=True)

    class Meta:
        model = Realty
        fields = ['id', 'realty_type', 'price', 'rooms_total',
                  'area_total', 'floor', 'floor_total', 'city', 'street', 'house', 'image']


class RealtyCRUDSerializer(serializers.ModelSerializer):
    image = ImageUrlField(many=True, read_only=True)
    finishing_type = serializers.CharField(source='finishing_type.title', max_length=50)
    method_selling = serializers.CharField(source='method_selling.title', max_length=50)
    city = serializers.CharField(source='address.city.title')
    street = serializers.CharField(source='address.street.title')
    house = serializers.CharField(source='address.house.title', allow_blank=True)

    class Meta:
        model = Realty
        fields = '__all__'

    def validate(self, attrs: dict):
        images = []
        valid_formats = ['png', 'jpeg', 'raw', 'jpg', 'tiff', 'psd', 'bmp', 'gif', 'png']
        if image_list := dict((self.initial_data).lists()).get('image'):
            for file in image_list:
                if isinstance(file, InMemoryUploadedFile):
                    if not any([True if file.name.lower().endswith(i) else False for i in valid_formats]):
                        raise ValidationError({'image': f'{file.name} is not a valid image format'})
                    images.append(file)

        attrs.update({'image': images})
        return attrs

    def create(self, validated_data):
        image_data = validated_data.pop('image')
        finishing_type = validated_data.pop('finishing_type')
        method_selling = validated_data.pop('method_selling')
        address = validated_data.pop('address')

        finishing_type_obj, _ = FinishingType.objects.get_or_create(title=finishing_type['title'])
        method_selling_obj, _ = MethodSelling.objects.get_or_create(title=method_selling['title'])

        city_obj, _ = City.objects.get_or_create(title=address['city']['title'])
        street_obj, _ = Street.objects.get_or_create(title=address['street']['title'])
        house_obj, _ = House.objects.get_or_create(title=address['house']['title'])

        address_obj, _ = Address.objects.get_or_create(city=city_obj, street=street_obj, house=house_obj)

        realty = Realty.objects.create(**validated_data,
                                       finishing_type=finishing_type_obj,
                                       method_selling=method_selling_obj,
                                       address=address_obj)

        for image in image_data:
            RealtyImage.objects.create(realty_id_id=realty.id, image=image)
        return realty

