from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from users.managers import CustomUserManager
import random

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email

class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def generate_code():
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])