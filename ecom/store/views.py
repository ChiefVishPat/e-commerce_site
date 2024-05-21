from django.shortcuts import render
from .models import Product
app_name = 'store'
def home(request):
    products = Product.objects.all()    #get all the products in the Product model 
    return render(request, 'home.html', {'products': products})