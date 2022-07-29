from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def realty_image_directory_path(instance, filename):
    return 'profiles/p_{0}/{1}'.format(instance.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    name = models.CharField("name", max_length=500, blank=True)
    surname = models.CharField("surname", max_length=500, blank=True)
    description = models.TextField("description", blank=True)
    phone = models.IntegerField("phone", validators=[
        MaxValueValidator(100_000_00_00),
        MinValueValidator(999_999_99_99)], null=True, blank=True)
    phone_verified = models.BooleanField("phone_verified", default=False)
    image = models.ImageField("image", upload_to=realty_image_directory_path, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
