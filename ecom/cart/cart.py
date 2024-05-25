#create a cart class that we can access throughout the website
from store.models import Product
class Cart():
    def __init__(self, request):
        #creating a session for the user
        self.session = request.session

        #get the current session key if it exists
        cart = self.session.get('session_key')

        #if the session key does not exist, create a new session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available on all pages of website
        self.cart = cart

    #gets the quantity of the cart
    def __len__(self):
        return len(self.cart)
    
    def get_quants(self):
        return self.cart
    
    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()

        #use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)

        return products

    #add a product to the cart
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #if the product is not in the cart, add it, else do nothing
        if product_id not in self.cart:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty) 
        else:
            pass

        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        user_cart = self.cart

        #update dictionary aka the cart
        user_cart[product_id] = product_qty

        self.session.modified = True
        return user_cart
    
    

