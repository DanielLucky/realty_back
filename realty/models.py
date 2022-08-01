from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from realty_back.settings import AUTH_USER_MODEL as User


class Realty(models.Model):
    title = models.CharField(max_length=50)  # *Название
    description = models.TextField()  # *Описание
    realty_type = models.CharField(max_length=4, choices=[
        ('rent', 'Аренда'),
        ('sale', 'Продажа')
    ], null=False)  # Тип объявления
    realty_format = models.CharField(max_length=10, choices=[
        ('flat', 'Квартира'),
        ('room', 'Комната'),
        ('cottages', 'Дома, дачи, коттеджи'),
        ('land', 'Земельные участки'),
        ('garages', 'Гаражи и машиноместа'),
        ('commercial', 'Коммерческая недвижимость')
    ], null=False)  # Тип недвижимости

    price = models.IntegerField(validators=[
        MinValueValidator(0)
    ])  # *Стоимость

    rooms_total = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
    ])  # *Кол-во комнат

    area_total = models.FloatField(validators=[
        MinValueValidator(1),
        MaxValueValidator(500)
    ])  # *Общая площадь
    area_kitchen = models.FloatField(validators=[
        MinValueValidator(1),
        MaxValueValidator(500)
    ])  # *Площадь кухни
    area_living = models.FloatField(validators=[
        MinValueValidator(1),
        MaxValueValidator(500)
    ])  # *Жилая площадь

    floor = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
    ])  # *Этаж
    floor_total = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
    ])  # *Этажей в доме

    balcony_or_loggia = models.CharField(max_length=2, choices=[
        ('bl', 'Балкон'),
        ('lg', 'Лоджия')
    ], null=False)  # Балкон или Лоджия

    window_type = models.CharField(max_length=4, choices=[
        ('yard', 'Во двор'),
        ('road', 'На дорогу')
    ], null=True)  # Окна

    bathroom = models.CharField(max_length=4, choices=[
        ('comb', 'Совмещенный'),
        ('sep', 'Раздельный')
    ], null=True)  # Санузел

    is_banned = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    finishing_type = models.ForeignKey('FinishingType', on_delete=models.PROTECT, null=False, related_name='finishing_type')  # Отделка
    method_selling = models.ForeignKey('MethodSelling', on_delete=models.PROTECT, null=True, related_name='method_selling')  # Метод продажи
    address = models.ForeignKey('Address', on_delete=models.PROTECT, null=True, related_name='address')  # Адрес TODO: Изменить на проде

    user = models.ForeignKey(User, on_delete=models.PROTECT)  #TODO: Изменить на проде

    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f'<Realty {self.id, self.title[:10]}>'


class FinishingType(models.Model):
    title = models.CharField(max_length=50, unique=True)  # *Название
    visibility = models.BooleanField(default=False)  # Отображение
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'<FinishingType {self.id, self.title, self.visibility}>'


class MethodSelling(models.Model):
    title = models.CharField(max_length=50)  # *Название
    visibility = models.BooleanField(default=False)  # Отображение
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'<MethodSelling {self.id, self.title[:5], self.visibility}>'


class Address(models.Model):
    city = models.ForeignKey('City', on_delete=models.PROTECT, null=True)  # Город
    street = models.ForeignKey('Street', on_delete=models.PROTECT, null=True)  # Улица
    house = models.ForeignKey('House', on_delete=models.PROTECT, null=True, blank=True)  # Номер дома

    def __str__(self):
        return f'<Address {self.id, self.city, self.street, self.house}>'


class City(models.Model):
    title = models.CharField(max_length=50)  # *Город
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'<City {self.id, self.title}>'


class Street(models.Model):
    title = models.CharField(max_length=50)  # *Улица
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'<Street {self.id, self.title}>'


class House(models.Model):
    title = models.CharField(max_length=50)  # *Номер дома
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'<House {self.id, self.title}>'


def realty_image_directory_path(instance, filename):
    return 'realty/r_{0}/{1}'.format(instance.realty.id, filename)


class RealtyImage(models.Model):
    realty = models.ForeignKey(Realty, related_name='image', on_delete=models.SET_NULL, unique=False, null=True)
    image = models.ImageField(upload_to=realty_image_directory_path)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['realty_id']
        ordering = ['image']

    def __str__(self):
        return str(self.image)
