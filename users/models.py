from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import Product


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', default='default.jpg', null=True, blank=True)
    address = models.CharField(max_length=200, default='', verbose_name='Адрес доставки')


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=300, default='')
    total_sum = models.IntegerField(default=0)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def sum(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Имя пользователя', null=True)
    order_sum = models.IntegerField(null=False, blank=False, default=0, verbose_name='Сумма заказа')
    order_quantity = models.IntegerField(null=False, blank=False, default=0, verbose_name='Количество товаров в заказе')
    delivery_address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Адрес доставки')
    order_date = models.CharField(max_length=20, null=True, blank=True, verbose_name='Дата заказа')
    products = models.ManyToManyField(Basket, verbose_name='Товары в заказе')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ для {self.username} {self.order_date}'


class OrderReturn(models.Model):
    ordername = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Название заказа', null=True)
    return_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата возврата')

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'

    def __str__(self):
        return f"Возврат заказа {self.ordername}"
