from django.shortcuts import render
from django.http.response import HttpResponse
from django.urls import path
from job.models import *
from public.test import str_to_int

# Create your views here.
ControlJobzhilian = JobzhilianController()

def index(request):
    return render(request, 'souJobs.html')

def Queryjob(request):
    jobName = request.GET.get('job')
    moneyInterval = request.GET.get('money_interval')
    count = str_to_int(request.GET.get('count'), 1)
    # if ControlJobzhilian.ClearJoblist(jobName):
    #     ControlJobzhilian.ReadFromDB(jobName)
    # datas = ControlJobzhilian.FilterData(jobName, '7000,11000')
    ControlJobzhilian.QueryJobsByPosition(position=jobName, money_interval=moneyInterval, limit=count)
    # ControlJobzhilian.Test(position=jobName, money_interval=moneyInterval)
    
    return HttpResponse(ControlJobzhilian.ListToJson(list=None, count=count), content_type='application/json')

def QueryJobAndWhere(request):
    pass

urlpatterns = [
    path('souJobs', index),
    path('Queryjob', Queryjob),
]