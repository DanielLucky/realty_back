import PIL
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers, status
from PIL import Image
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from realty_back import settings
from .models import *


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.title')
    street = serializers.CharField(source='street.title')
    house = serializers.CharField(source='house.title', allow_blank=True)

    class Meta:
        model = Address
        fields = ['city', 'street', 'house']


class ImageUrlField(serializers.ModelSerializer):

    class Meta:
        model = RealtyImage
        fields = ['image', ]

    def to_representation(self, instance):
        return 'http://127.0.0.1:8000' + settings.MEDIA_URL + instance.image.name  # TODO: Изменить на проде


class RealtySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    city = serializers.CharField(source='address.city.title')
    street = serializers.CharField(source='address.street.title')
    house = serializers.CharField(source='address.house.title', allow_blank=True)

    def get_image(self, instance):
        items = RealtyImage.objects.filter(realty=instance, visible=True)
        serializer = ImageUrlField(instance=items, many=True)
        return serializer.data

    class Meta:
        model = Realty
        fields = ['id', 'realty_type', 'price', 'rooms_total',
                  'area_total', 'floor', 'floor_total', 'city', 'street', 'house', 'image']


class RealtyCRUDSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    finishing_type = serializers.CharField(source='finishing_type.title', max_length=50)
    method_selling = serializers.CharField(source='method_selling.title', max_length=50)
    city = serializers.CharField(source='address.city.title')
    street = serializers.CharField(source='address.street.title')
    house = serializers.CharField(source='address.house.title', allow_blank=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def get_image(self, instance):
        items = RealtyImage.objects.filter(realty=instance, visible=True)
        serializer = ImageUrlField(instance=items, many=True)
        return serializer.data

    class Meta:
        model = Realty
        exclude = ('address', )
        # fields = '__all__'

    def validate(self, attrs: dict):
        images = []
        valid_formats = ['png', 'jpeg', 'raw', 'jpg', 'tiff', 'psd', 'bmp', 'gif', 'png']
        if not attrs:
            raise ValidationError({'params': 'parameters not passed'})

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
            RealtyImage.objects.create(realty=realty, image=image)
        return realty

    def update(self, instance: Realty, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.realty_type = validated_data.get('realty_type', instance.realty_type)
        instance.realty_format = validated_data.get('realty_format', instance.realty_format)
        instance.price = validated_data.get('price', instance.price)
        instance.rooms_total = validated_data.get('rooms_total', instance.rooms_total)
        instance.area_total = validated_data.get('area_total', instance.area_total)
        instance.area_kitchen = validated_data.get('area_kitchen', instance.area_kitchen)
        instance.area_living = validated_data.get('area_living', instance.area_living)
        instance.floor = validated_data.get('floor', instance.floor)
        instance.floor_total = validated_data.get('floor_total', instance.floor_total)
        instance.balcony_or_loggia = validated_data.get('balcony_or_loggia', instance.balcony_or_loggia)
        instance.window_type = validated_data.get('window_type', instance.window_type)
        instance.bathroom = validated_data.get('bathroom', instance.bathroom)

        if 'image' in validated_data:
            RealtyImage.objects.filter(realty=instance).update(visible=False)  # Скрытие старых фото
            for image in validated_data.get('image'):
                RealtyImage.objects.create(realty=instance, image=image)

        if finishing_type_data := validated_data.get('finishing_type'):
            if finishing_type_data.get('title') != instance.finishing_type.title:
                finishing_type_obj, _ = FinishingType.objects.get_or_create(title=finishing_type_data['title'])
                instance.finishing_type = finishing_type_obj

        if method_selling_data := validated_data.get('method_selling'):
            if method_selling_data.get('title') != instance.method_selling.title:
                method_selling_obj, _ = MethodSelling.objects.get_or_create(title=method_selling_data['title'])
                instance.method_selling_data = method_selling_obj

        if address := validated_data.get('address'):
            address_obj = Address.objects.get(realty=instance)
            if city_data := address.get('city'):
                if city_data.get('title') != instance.address.city.title:
                    city_obj, _ = City.objects.get_or_create(title=city_data['title'])
                    address_obj.city = city_obj

            if street_data := address.get('street'):
                if street_data.get('title') != instance.address.street.title:
                    street_obj, _ = Street.objects.get_or_create(title=street_data['title'])
                    address_obj.street = street_obj

            if house_data := address.get('house'):
                if house_data.get('title') != instance.address.house.title:
                    house_obj, _ = House.objects.get_or_create(title=house_data['title'])
                    address_obj.house = house_obj
            address_obj.save()

            instance.address = address_obj
        instance.save()

        return instance
