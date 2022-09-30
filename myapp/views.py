from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import ProductModel

# Create your views here.

def index(request):
    products = ProductModel.objects.all()
    productlist = []
    for i in range(1, 9):
        product = ProductModel.objects.get(id = i)
        productlist.append(product)
    return render(request, 'index.html', locals())

def detail(request, id=None):
    product = ProductModel.objects.get(id = id)
    return render(request, 'detail.html', locals())

