from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

app_name = 'store'

#directs to the home page
def home(request):
    products = Product.objects.all()    #get all the products in the Product model
    return render(request, 'home.html', {'products': products})

#directs to the about page
def about(request):
    return render(request, 'about.html')

#handles a login request
def login_user(request):
    if request.method == 'POST':    #basically checks if the user has pressed the submit button to POST the information
        username = request.POST['username']
        password = request.POST['password']
        # authenticate the user
        user = authenticate(request, username=username, password=password)  #authenticates the user

        #this if/else statement checks to see if the user is valid or invalid and handle the request accordingly
        #login was successful
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        #login is unsuccessful
        else:
            messages.success(request, ("Error logging in - Please try again"))
            return redirect('login')
    #else log in as normal --> user has not clicked the submit button and most likely has clicked the login button in the navbar
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully been logged out!"))
    return redirect('home')