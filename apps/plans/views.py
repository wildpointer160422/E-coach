from django.shortcuts import render
from .models import Plan

# Create your views here.
def index(request):
    plans = Plan.objects.all()
    return render(request, 'plans/plan_select.html', {'plans': plans})

def input_rm(request):
    return render(request, 'plans/input_rm.html')

def weekly_plan(request):
    return render(request, 'plans/weekly_plan.html')
