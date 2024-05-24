from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    return render(request, 'cart_summary.html', {})

def cart_add(request):
    #get the cart
    cart = Cart(request)

    #test for POST
    if request.POST.get('action') == 'post':
        #get the product_id from the form
        product_id = int(request.POST.get('product_id'))    #product_id from store/templates/product.html

        #get the product from the database
        product = get_object_or_404(Product, id=product_id)

        #add the product to the cart in the session
        cart.add(product=product)

        #get cart quantity
        cart_quantity = cart.__len__()

        #return the response
        # response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})
        return response 


    return render(request, )

def cart_delete(request):
    pass

def cart_update(request):
    pass
