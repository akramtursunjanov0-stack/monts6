from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategoryListSerializers, CategoryDetailSerializers, ProductListSerializers, ProductDetailSerializers
from .serializers import ReviewListSerializers, ReviewDetailSerializers
from .serializers import ProductValidateSerializer, ReviewListSerializers, CategoryValidateSerializer, ReviewValidateSerializer
from rest_framework.viewsets import ModelViewSet


# Если поступает гет запрос по данной функции - обрабатываем, иначе пропускаем
@api_view(['GET'])
# Функция
def shop_products_with_reviews_view(request):
    #оптимизация запросов
    products = Product.objects.prefetch_related('reviews').all()
    
    # ручное формирование данных через цикл
    result = []
    for product in products:
        reviews = product.reviews.all()
        
        # проверка
        if reviews:
            # вычисления
            average_rating = sum(review.stars for review in reviews) / len(reviews)
            average_rating = round(average_rating, 1)
        else:
            # если не вычислели - передам ничего
            average_rating = None
        
        # сериализация данных
        reviews_data = ReviewListSerializers(reviews, many=True).data
        product_data = ProductListSerializers(product).data
        

        product_data['reviews'] = reviews_data # Добавляем список отзывов
        product_data['average_rating'] = average_rating # Добавляем средний рейтинг
        # Добавления результатов 
        result.append(product_data)
    
    return Response(data=result)


class ShopListCategoryView(ModelViewSet):
    queryset = Category.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializers
        return CategoryDetailSerializers

@api_view(['GET', 'POST'])
def shop_list_category_view(request):
    # Вытаскиваем все объекты
    if request.method == 'GET':
        category = Category.objects.all()
        # Формотируем все объекты
        data = CategoryListSerializers(category, many=True).data
        # проходимся через цикл, через встроенную функцию enumerate получаем индексы и cat
        for i, cat in enumerate(category):
            data[i]['products_count'] = cat.products.count()
        # Отправляем все в json формате 
        return Response(data=data)
    elif request.method == 'POST':

        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.errors)
        name = request.data.get('name')

        category = Category.objects.create(
            name=name
        )

        return Response(status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def shop_detail_category_view(request, id):
    try:
        category_one = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'not exsist this table'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailSerializers(category_one).data
        data['products_count'] = category_one.products_count
        return Response(data=data)
    elif request.method == 'DELETE':
        category_one.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.errors)
        category_one.name = request.data.get('name')
        category_one.save()
        return Response(status=status.HTTP_201_CREATED)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('category')
    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializers
        return ProductDetailSerializers

@api_view(['GET', 'POST'])
def shop_list_product_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        data = ProductListSerializers(product, many=True).data
        return Response(data=data)
    elif request.method == 'POST':

        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category = request.data.get('category')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price
        )
        product.category.set(category)
        product.save()

        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def shop_detatil_product_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Не найден айди'})
    if request.method == 'GET':
        data = ProductDetailSerializers(product).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':

        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return Response(status=status.HTTP_404_NO_CONTENT, data=serializer.errors)
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category.set(request.data.get('category'))
        product.save()
        return Response(status=status.HTTP_201_CREATED)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related('product')

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializers
        return ReviewDetailSerializers

@api_view(['GET', 'POST'])
def shop_list_review_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewListSerializers(review, many=True).data
        return Response(data=data)
    elif request.method == 'POST':

        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        text = request.data.get('text')
        product = request.data.get('product')
        stars = request.data.get('stars')

        review = Review.objects.create(
            text=text,
            product_id=product,
            stars=stars
        )

        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PUT'])
def shop_detatil_review_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Не найден айди'})
    if request.method == 'GET':
        data = ReviewDetailSerializers(review).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        review.text = request.data.get('title')
        review.product = request.data.get('description')
        review.price = request.data.get('price')
        review.save()
        return Response(status=status.HTTP_201_CREATED)    