from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
# Create your views here.

def index(request):
    template = loader.get_template('base.html')
    #return HttpResponse(template.render())
    return HttpResponse("hello world")