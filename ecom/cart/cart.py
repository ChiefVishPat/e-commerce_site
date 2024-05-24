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