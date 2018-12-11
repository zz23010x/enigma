from django.shortcuts import render
from django.http.response import HttpResponse
from django.urls import path
from shop.models import *
from public.test import str_to_int

ControlShop = ShopController()
# Create your views here.
def index(request):
    return render(request, 'shop/login.html')

def LoginSystem(request):
    UserName = request.GET.get('username')
    PassWord = request.GET.get('password')
    if 'sell' in UserName:
        return render(request, 'shop/merchandisemanagem.html')
    elif 'buy' in UserName:
        return render(request, 'shop/shopping.html')
    return render(request, 'shop/login.html')

def QueryGoodsList(request):
    return HttpResponse(ControlShop.ListToJson(), content_type='application/json')

urlpatterns = [
    path('login', index),
    path('LoginSystem', LoginSystem),
    path('QueryGoodsList', QueryGoodsList),
]