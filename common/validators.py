from datetime import date
from rest_framework.exceptions import ValidationError


def validate_user_age(user):

    if not user.birthdate:
        raise ValidationError("У пользователя не указана дата рождения")

    today = date.today()

    age = today.year - user.birthdate.year

    if age < 18:
        raise ValidationError(
            "Пользователь должен быть старше 18 лет для создания продукта"
        )