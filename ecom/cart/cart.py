#create a cart class that we can access throughout the website
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

    #add a product to the cart
    def add(self, product):
        product_id = str(product.id)

        #if the product is not in the cart, add it, else do nothing
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price)}
        else:
            pass

        self.session.modified = True