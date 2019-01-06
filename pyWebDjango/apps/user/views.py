from django.shortcuts import render
from django.urls import path
from django.http.response import HttpResponse
from user.models import *
import json

# Create your views here.
def admin(request):
    return render(request, 'admin.html')

def login(request):
    # User.objects.create(name="asdasd", price=20, account="asdasd", password="asdasd", authority=1)
    # a = User.objects.get(name="asdasd")
    # c = request.GET.get('username')
    # return HttpResponse(c)
    # a = User.objects.all()
    # list = [] 
    # str1 = ''
    # for i in a:
    #     dict = {'id' : i.id, 'name':i.name, 'account':i.account}
    #     list.append(dict)
    # return HttpResponse(json.dumps(list), content_type='application/json')
    return render(request, 'shop.html')

def ClearDataBase(request):
    from public.sqlite3Helper import DataBaseServer
    DataBaseServer().DropAllTables()
    return render(request, 'admin.html')

def UpdateJobs(request):
    from job.models import JobzhilianController
    ControlJobzhilian = JobzhilianController()
    ControlJobzhilian.UpdateJobsInfo('测试')
    return render(request, 'admin.html')

urlpatterns = [
    path('admin', admin),
    path('ClearDataBase', ClearDataBase),
    path('UpdateJobs', UpdateJobs),
]