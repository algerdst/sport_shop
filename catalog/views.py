import datetime
import io

from django.contrib import messages
from django.forms import model_to_dict
from django.http import FileResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from rest_framework import generics, viewsets
from rest_framework.views import APIView

from .serializers import *
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from users.models import Basket, Order

from .forms import SearchForm
from .models import Brand, Category, ItemType, Product

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


def index(request):
    """
    Отображает главную старницу
    """
    try:
        products = Product.objects.filter(name__icontains=request.GET['search'])
    except:
        products = Product.objects.all()
    form = SearchForm()
    categories = Category.objects.all()
    items_types = ItemType.objects.all()
    brands = Brand.objects.all()
    data = {
        'products': products,
        'categories': categories,
        'items_types': items_types,
        'brands': brands,
        'form': form
    }
    return render(request, 'catalog/index.html', context=data)


def category_filter(request, slug):
    """
    Отображает старницу c фильтром по категориям
    """
    form = SearchForm()
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    items_types = ItemType.objects.all()
    brands = Brand.objects.all()
    data = {
        'products': products,
        'categories': categories,
        'items_types': items_types,
        'brands': brands,
        'form': form
    }
    return render(request, 'catalog/index.html', context=data)


def item_types_filter(request, slug):
    """
    Отображает старницу c фильтром по типам
    """
    form = SearchForm()
    item_type = ItemType.objects.get(slug=slug)
    products = Product.objects.filter(type_product=item_type)
    categories = Category.objects.all()
    items_types = ItemType.objects.all()
    brands = Brand.objects.all()
    data = {
        'products': products,
        'categories': categories,
        'items_types': items_types,
        'brands': brands,
        'form': form
    }
    return render(request, 'catalog/index.html', context=data)


def brand_filter(request, slug):
    """
    Отображает старницу c фильтром по брендам
    """
    form = SearchForm()
    brand = Brand.objects.get(slug=slug)
    products = Product.objects.filter(brand=brand)
    categories = Category.objects.all()
    items_types = ItemType.objects.all()
    brands = Brand.objects.all()
    data = {
        'products': products,
        'categories': categories,
        'items_types': items_types,
        'brands': brands,
        'form': form
    }
    return render(request, 'catalog/index.html', context=data)


def product(request, slug):
    product = Product.objects.get(slug=slug)
    data = {
        'product': product
    }
    return render(request, 'catalog/product.html', context=data)


def basket_add(request, product_id):
    """
    Отвечает за кнопку добавления товара в корзину
    """
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        baskets = Basket.objects.filter(user=request.user, product=product)
        if not baskets.exists():
            Basket.objects.create(user=request.user, product=product, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('authorization'))


def basket_remove(request, basket_id):
    """
    Отвечает за кнопку удаления товара из корзины
    """
    basket = Basket.objects.get(id=basket_id)
    Basket.delete(basket)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def make_order(request):
    """
    Отвечает за кнопку оформления заказа
    После нажатия кнопки, генерируется pdf документ с деталями заказа
    """
    baskets = Basket.objects.filter(user=request.user)  # Получаем все позиции, которые пользователь хочет заказать
    for basket in baskets:
        product = basket.product  # Название заказываемого товара
        product_quantity_on_stock = basket.product.quantity_in_stock  # Количество заказываемого товара на складе
        quantity_in_basket = basket.quantity  # Количество заказываемого товара на складе
        new_quantity_on_stock = product_quantity_on_stock - quantity_in_basket  # Количество на складе после заказа
        if new_quantity_on_stock < 0:  # Если количество товара на складе меньше чем в заказе, переходим в цикл
            messages.error(request,
                           f'Недостаточное количество товара {product} на складе, выберите меньшее количество или обратитесь в магазин')  # Передаем в шаблон сообщение
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            product_id = basket.product.id
            edit_product = Product.objects.get(id=product_id)
            edit_product.quantity_in_stock = new_quantity_on_stock
            edit_product.save()
    total_sum = sum([basket.sum() for basket in baskets])
    total_quantity = sum([basket.quantity for basket in baskets])
    now = str(datetime.datetime.now())[:16]
    order = Order(username=request.user, order_sum=total_sum, order_quantity=total_quantity, delivery_address='Москва',
                  order_date=now)
    order.save()
    for basket in baskets:
        order.products.add(basket)
    order.save()
    user_name = request.user.username
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Arial', 12)
    p.drawString(430, 800, f"Дата {now}")
    p.setFont('Arial', 21)
    p.drawString(240, 750, f"Товарный чек")
    p.setFont('Arial', 14)
    p.drawString(30, 650, f"Наименование товара                      |")
    p.drawString(290, 650, f"Количество      |")
    p.drawString(420, 650, f"Цена      |")
    p.drawString(510, 650, f"Сумма      |")

    string = 600
    for basket in baskets:
        product = basket.product.name
        quantity = basket.quantity
        price = basket.product.price
        summa = basket.product.price * quantity
        p.drawString(30, string, f"{product}")
        p.drawString(320, string, f"{quantity}")
        p.drawString(430, string, f"{price}")
        p.drawString(520, string, f"{summa}")
        string -= 50
    p.drawString(30, string, f"Имя:    {request.user.first_name}")
    p.drawString(30, string - 50, f"Фамилия:    {request.user.last_name}")
    p.drawString(30, string - 100, f"Адрес доставки:    {request.user.address}")
    p.drawString(30, string - 150, f"Всего {total_quantity} товаров на {total_sum} руб.")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Заказ для {user_name}.pdf")


def return_order(request, order_id):
    """
    Функция для кнопки 'Отменить заказ'
    Возвращает все заказанные товары на склад
    и удаляет заказ
    """
    order = Order.objects.get(id=order_id)
    baskets = order.products.all()
    for basket in baskets:
        basket_product = basket.product.id
        basket_quantity = basket.quantity
        product = Product.objects.get(id=basket_product)
        product.quantity_in_stock += basket_quantity
        product.save()
    order.delete()

    return HttpResponseRedirect(reverse('profile'))


def save_pdf(request, order_id):
    """
    Отвечает за кнопку сохранить PDF
    """
    order = Order.objects.get(id=order_id)
    baskets = order.products.all()
    total_sum = sum([basket.sum() for basket in baskets])
    total_quantity = sum([basket.quantity for basket in baskets])
    now = str(datetime.datetime.now())[:19]
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Arial', 20)
    user_name = request.user.username
    p.drawString(100, 100, f"Заказ для {user_name}")
    p.drawString(100, 200, f"Итоговая сумма {total_sum}")
    p.drawString(100, 300, f"Количество товаров {total_quantity}")
    p.drawString(100, 400, f"Адрес доставки {request.user.address}")
    p.drawString(100, 500, f"Дата доставки {now}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Заказ для {user_name}.pdf")


def get_mark(request, mark_id, product_id):
    product = Product.objects.get(id=product_id)
    product.calculate_mark(new_mark=mark_id)
    product.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# ----------------api----------------

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    #Отдает все категории
    @action(methods=['get'], detail=False)
    def categories(self, request):
        categories = Category.objects.all()
        return Response({'categories': [cat.category_name for cat in categories]})

    # Отдает одну категорию по id
    @action(methods=['get'], detail=True)
    def category(self, request, pk):
        category = Category.objects.get(pk=pk)
        return Response({'category': category.category_name})

    #Отдает список товаров по слагу категории
    @action(methods=['get'], detail=True)
    def product_category(self, request, pk):
        category = Category.objects.get(slug=pk)
        products = Product.objects.filter(category=category)
        return Response({'category': [{prod.name: prod.slug} for prod in products]})

    # Отдает все бренды
    @action(methods=['get'], detail=False)
    def brand(self, request):
        brands = Brand.objects.all()
        return Response({'categories': [brand.brand_name for brand in brands]})

