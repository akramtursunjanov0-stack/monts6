from django.contrib.auth.models import BaseUserManager, UserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email requeired!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Number phone not found!")
        user = self.model(phone_number=phone_number, email=email, password=password)
        user.set_password(password)
        
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save()

        return user