from django.shortcuts import render
from django.http import HttpResponse
import math

# Create your views here.
def main(request):
    return render(request, template_name='main.html')

def hello(request):
    return HttpResponse('привет- привет!')

def pi(request):
    pi_value = math.pi
    return HttpResponse(f'Число пи: {pi_value}')

def name(request):
    myname = 'Антона Макридина'

    context = {'name_template': myname}
    return render(request, 'mytpl.html', context)