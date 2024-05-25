from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    #get the cart
    cart = Cart(request)

    #test for POST
    if request.POST.get('action') == 'post':
        #get the product_id from the form
        product_id = int(request.POST.get('product_id'))    #product_id from store/templates/product.html
        product_qty = int(request.POST.get('product_qty'))    #product_qty from store/templates/product.html

        #get the product from the database
        product = get_object_or_404(Product, id=product_id)

        #add the product to the cart in the session
        cart.add(product=product, quantity=product_qty)

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
    #get the cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        #get the product_id from the form
        product_id = int(request.POST.get('product_id'))  
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({'qty': product_qty})
        return response
    
def cart_delete(request):
    #get the cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        #get the product_id from the form
        product_id = int(request.POST.get('product_id'))

        #call delete func from Cart 
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        return response