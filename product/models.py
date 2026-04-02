from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    # создаем поле 


    def __str__(self):
        return self.name # вызываем магический метод
    

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = 'Категирии'


    
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ManyToManyField(Category,related_name='products')


    def __str__(self):
        return self.title 
    


class Review(models.Model):
    choices = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    text = models.TextField()
    product = models.ForeignKey(Product , on_delete=models. CASCADE, related_name='reviews', null=True)

    star = models.IntegerField(choices=choices,default=1, null=True)

    def __str__(self):
        return f"отзыв"