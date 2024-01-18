from django.db import models


class Brand(models.Model):
    brand_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Название бренда')
    slug = models.SlugField(default='')

    class Meta:
        verbose_name = 'Название бренда'
        verbose_name_plural = 'Названия брендов'

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название категории')
    slug = models.SlugField(default='')
    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'
    def __str__(self):
        return self.category_name


class ItemType(models.Model):
    type_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Тип товара')
    categories=models.ManyToManyField(Category, default='')
    slug = models.SlugField(default='')

    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

    def __str__(self):
        return self.type_name


class PopularCategory(models.Model):
    popular_category_name = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Популярная категория')

    class Meta:
        verbose_name = 'Популярная категория'
        verbose_name_plural = 'Популярные категории'

    def __str__(self):
        return self.popular_category_name.category_name


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Название товара')
    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL, verbose_name='Название бренда')
    type_product = models.ForeignKey(ItemType, null=True, on_delete=models.SET_NULL, verbose_name='Тип товара')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, verbose_name='Категория товара')
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')
    quantity_in_stock = models.IntegerField(null=True, blank=True, verbose_name='Количество товара на складе')
    description = models.CharField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    mark = models.SmallIntegerField(default=0, verbose_name='Оценка товара')
    marks_count = models.IntegerField(default=0, verbose_name='Количество оценок')
    marks_sum = models.IntegerField(default=0, verbose_name='Сумма оценок')
    slug = models.SlugField(default='')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def calculate_mark(self, new_mark):
        self.marks_sum += new_mark
        self.marks_count += 1
        self.mark = round(self.marks_sum / self.marks_count)


class Gallery(models.Model):
    image = models.ImageField(upload_to='product_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url
