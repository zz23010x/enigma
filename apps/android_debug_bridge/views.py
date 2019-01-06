from django.shortcuts import render
from django.urls import path

# Create your views here.
def index(request):
    return render(request, 'terminal_adb.html')
    
urlpatterns = [
    path('adbt', index),
]