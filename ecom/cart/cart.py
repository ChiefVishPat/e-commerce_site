#create a cart class that we can access throughout the website
from store.models import Product, Profile
class Cart():
    def __init__(self, request):
        #creating a session for the user
        self.session = request.session

        #get request
        self.request = request

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
    
    def cart_total(self):
        product_ids = self.cart.keys()  #get product ids in the cart
        products = Product.objects.filter(id__in=product_ids)   #lookup the keys in our products database model based off of the cart
        qtys = self.cart    #get the quantities
        total = 0

        for key, value in qtys.items():
            key = int(key)  #make sure product gets passed as int
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value

        return total
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

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

        #Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            curr_user = Profile.objects.filter(user__id=self.request.user.id)

            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            curr_user.update(old_cart=str(carty))

    #update product quantities in cart
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        user_cart = self.cart

        #update dictionary aka the cart
        user_cart[product_id] = product_qty

        self.session.modified = True
        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

        return user_cart
    
    #delete a product from the cart
    def delete(self, product):
        product_id = str(product)

        #if the product is in the cart, delete it
        if product_id in self.cart:
            del self.cart[product_id]
        else:
            pass

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

