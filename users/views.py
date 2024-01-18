from django.contrib import auth, messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm

from .models import Basket, Order


def authorization(request):
    """
    Авторизация пользователя
    """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = UserLoginForm()
    data = {
        'form': form
    }
    return render(request, template_name='users/authorization.html', context=data)


def registration(request):
    """
    Регистрация пользователя
    """
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return HttpResponseRedirect(reverse('authorization'))
    else:
        form = UserRegistrationForm()
    data = {
        'form': form
    }
    return render(request, 'users/registration.html', context=data)


def profile(request):
    """
    Профиль пользователя
    """
    if request.user.is_authenticated:
        user = request.user
        baskets = Basket.objects.filter(user=request.user)
        total_sum = sum([basket.sum() for basket in baskets])
        total_quantity = sum([basket.quantity for basket in baskets])
        orders = Order.objects.filter(username=request.user.id)
        data = {
            'user': user,
            'baskets': Basket.objects.filter(user=request.user),
            'total_sum': total_sum,
            'total_quantity': total_quantity,
            'orders': orders
        }
    else:
        return HttpResponseRedirect(reverse('authorization'))
    return render(request, 'users/profile.html', context=data)


def logout(request):
    """
    Выход из профиля
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('home'))


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        baskets = Basket.objects.filter(user=request.user)
        total_sum = sum([basket.sum() for basket in baskets])
        total_quantity = sum([basket.quantity for basket in baskets])
        data = {
            'user': user,
            'baskets': Basket.objects.filter(user=request.user),
            'total_sum': total_sum,
            'total_quantity': total_quantity,
        }
    else:
        return HttpResponseRedirect(reverse('authorization'))
    return render(request, 'users/basket.html', context=data)
