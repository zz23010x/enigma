from django.shortcuts import render
from django.urls import path
from django.http.response import HttpResponse
from souzr.models import *
from public.test import str_to_int
import json

# Create your views here.
def index(request):
    return render(request, 'sou.html')

def Querysouzr(request):
    addr = request.GET.get('addr')
    bus = request.GET.get('busline')
    price_min = str_to_int(request.GET.get('price_min'), 0)
    price_max = str_to_int(request.GET.get('price_max'), 99999)
    count = str_to_int(request.GET.get('count'), 1)
    ControlRoom = ZiroomController()
    if addr != '':
        roomlist = ControlRoom.QueryRoomsByAddr(address=addr, price_min=price_min, price_max=price_max, limit=count)
    elif bus != '':
        roomlist = ControlRoom.QueryRoomsByBus(busline=bus, price_min=price_min, price_max=price_max, limit=count)
    
    return HttpResponse(json.dumps(roomlist), content_type='application/json')

urlpatterns = [
    path('sou', index),
    path('Querysouzr', Querysouzr),
]