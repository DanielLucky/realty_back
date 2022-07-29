from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('The given not correct email must be set')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        # проверяем является ли пользователь
        # суперпользователем
        if extra_fields.get('is_superuser'):
            user = self.model(
                email=email,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            username=username,
            password=password,
            **extra_fields
        )
