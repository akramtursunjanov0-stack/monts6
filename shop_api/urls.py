"""
URL configuration for shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product import views

router = DefaultRouter()
# Регистрируем КАЖДЫЙ ViewSet отдельным вызовом
router.register('categories', views.ShopListCategoryView)  # Первый вызов
router.register('products', views.ProductViewSet)          # Второй вызов
router.register('reviews', views.ReviewViewSet)            # Третий вызов

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/', views.shop_list_category_view), # GET - list, POST - create
    path('api/v1/categories/<int:id>/', views.shop_detail_category_view),
    path('api/v1/products/', views.shop_list_product_view),
    path('api/v1/products/<int:id>/', views.shop_detatil_product_view),
    path('api/v1/reviews/', views.shop_list_review_view),
    path('api/v1/reviews/<int:id>/', views.shop_detatil_review_view),
    path('api/v1/products/reviews/', views.shop_products_with_reviews_view),
    path('api/v2/', include(router.urls)),  # Подключаем ВСЕ зарегистрированные маршруты
    path('api/v1/users/', include('users.urls')),
]