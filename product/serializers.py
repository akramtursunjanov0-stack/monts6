from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError



# Создаем класс категори деталей, чтобы вывести все значения в json формате
class CategoryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Создаем класс CategoryListSerializers, чтобы вывести все значения в json формате
class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Создаем класс ProductListSerializers, чтобы вывести все значения в json формате
class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Создаем класс ProductDetailSerializers, чтобы вывести все значения в json формате
class ProductDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Создаем класс ReviewListSerializers, чтобы вывести все значения в json формате
class ReviewListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'product', 'stars']

# Создаем класс ReviewDetailSerializers, чтобы вывести все значения в json формате
class ReviewDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# Создаем класс ReviewSerializers, чтобы вывести значения id text product stars в json формате
class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id text product stars']

# Создаем класс ReviewSerializers, чтобы вывести все значения в json формате
class ProductWithReviewsSerializer(serializers.ModelSerializer):
    # Проходимся по каждому айди, тексту, продукту, отзыву, чтобы зафиксировать это в БД
    reviews = ReviewSerializers(many=True)
    # Когда запросят запрос - создатся, до этого по просту этой переменной нету. Нужен чтобы не хранить пустый бессконечный рейтинг
    # Проще говоря, создался - сделал - ушел
    average_rating = serializers.SerializerMethodField()

    # Обычный класс мета
    class Meta:
        model = Product
        fields = ['__all__']

    # функция для получения среднего значения
    def get_average_rating(self, obj):
        # Получаем все отзывы по данную значению
        reviews = obj.reviews.all()
        # Делаем проверку, если есть значение
        if reviews:
            # Возвращаем среднее арифмитическое
            # sum - суммирует, внутри цикл генерирует списки, и проходит по всем спискам, после делим на все отзывы
            return sum(review.stars for review in reviews) / len(reviews)
        # иначе вернем - ничего
        return None


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=3)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField()
    category = serializers.ListField(child=serializers.IntegerField())

    def validate_category(self, category):
        category = list(set(category))
        category_from_db = Category.objects.filter(id__in=category)
        if len(category) != len(category_from_db):
            raise ValidationError("Category does not exsist")
        return category


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True
    )
    stars = serializers.ChoiceField(choices=Review.choices, default=1)
    
    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Текст отзыва должен быть не менее 10 символов")
        return value


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=10)