from rest_framework import serializers
from users.models import CustomUser
from rest_framework.exceptions import ValidationError

class RegistrationSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise ValidationError("Пользователь уже существует!")
    