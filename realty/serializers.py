from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from realty_back import settings
from .models import *


class AddressNewSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.title', max_length=50)
    street = serializers.CharField(source='street.title', max_length=50)
    house = serializers.CharField(source='house.title', max_length=50)

    class Meta:
        model = Address
        exclude = ['id', ]

    def save(self, instance, validated_data):
        city_obj, _ = City.objects.get_or_create(title=validated_data['city'])
        street_obj, _ = Street.objects.get_or_create(title=validated_data['street'])
        house_obj, _ = House.objects.get_or_create(title=validated_data['house'])
        address_obj, _ = Address.objects.get_or_create(city=city_obj, house=house_obj, street=street_obj)
        return address_obj


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
    is_banned = serializers.BooleanField(read_only=True)
    is_visible = serializers.BooleanField(read_only=True)

    def get_image(self, instance):
        items = RealtyImage.objects.filter(realty=instance, visible=True)
        serializer = ImageUrlField(instance=items, many=True)
        return serializer.data

    class Meta:
        model = Realty
        exclude = ['title', 'description', 'area_kitchen', 'area_living', 'balcony_or_loggia', 'window_type',
                   'bathroom', 'finishing_type', 'method_selling', 'address', 'updated_at']


class RealtyCRUDSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    finishing_type = serializers.CharField(source='finishing_type.title', max_length=50, required=True)
    method_selling = serializers.CharField(source='method_selling.title', max_length=50, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    city = serializers.CharField(source='address.city.title')
    street = serializers.CharField(source='address.street.title')
    house = serializers.CharField(source='address.house.title', allow_blank=True)

    class Meta:
        model = Realty
        exclude = ['is_banned', ]

    def get_image(self, instance):
        items = RealtyImage.objects.filter(realty=instance, visible=True)
        serializer = ImageUrlField(instance=items, many=True, allow_null=True)
        return serializer.data

    def validate(self, attrs: dict):
        images = []
        valid_formats = ['png', 'jpeg', 'raw', 'jpg', 'tiff', 'psd', 'bmp', 'gif', 'png']
        if not attrs:
            raise ValidationError({'params': 'parameters not passed'})
        if self.initial_data.get('image'):
            for file in dict((self.initial_data).lists()).get('image'):
                if isinstance(file, InMemoryUploadedFile):
                    if not any([True if file.name.lower().endswith(i) else False for i in valid_formats]):
                        raise ValidationError({'image': f'{file.name} is not a valid image format'})
                    images.append(file)

        attrs.update({'image': images})

        address = AddressNewSerializer(data={
            'city': attrs['address']['city']['title'],
            'street': attrs['address']['street']['title'],
            'house': attrs['address']['house']['title']})
        address.is_valid(raise_exception=True)
        attrs.update({'address': address})
        return attrs

    def create(self, validated_data):
        image_data = validated_data.pop('image')

        validated_data['finishing_type'], _ = FinishingType.objects.get_or_create(
            title=validated_data['finishing_type']['title'])
        validated_data['method_selling'], _ = MethodSelling.objects.get_or_create(
            title=validated_data['method_selling']['title'])

        validated_data['address'] = validated_data['address'].save(
            validated_data['address'],
            validated_data['address'].data)

        realty_obj = Realty.objects.create(**validated_data)

        for image in image_data:
            RealtyImage.objects.create(realty=realty_obj, image=image)

        return realty_obj

    def update(self, instance: Realty, validated_data):
        if 'image' in validated_data:
            RealtyImage.objects.filter(realty=instance).update(visible=False)  # Скрытие старых фото
            for image in validated_data.get('image'):
                RealtyImage.objects.create(realty=instance, image=image)

        finishing_type_obj, _ = FinishingType.objects.get_or_create(title=validated_data['finishing_type']['title'])
        validated_data['finishing_type'] = finishing_type_obj
        method_selling_obj, _ = MethodSelling.objects.get_or_create(title=validated_data['method_selling']['title'])
        validated_data['method_selling'] = method_selling_obj

        validated_data['address'] = validated_data['address'].save(
            validated_data['address'],
            validated_data['address'].data)

        del validated_data['image']
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class RealtyCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        exclude = ['created_at', ]


@api_view(['GET'])
def realty_search(request):
    """
    Поиск недвижимости
    :param request:
    :return:
    """
    return Response({"message": "Hello for today! See you tomorrow!"})