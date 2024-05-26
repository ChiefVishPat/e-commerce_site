from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django.contrib import messages

app_name = 'store'

def category_summary(request):
    categories = Category.objects.all() #grab all the categories from the Category db model
    return render(request, 'category_summary.html', {'categories': categories})

def category(request, foo):
    foo = foo.replace('-', ' ')     #replace '-' with spaces

    #grab the category from the url
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'category': category, 'products': products})
    except:
        messages.success(request, ("That category does not exist"))
        return redirect('home')
    

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

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

def register_user(request):
    form = SignUpForm()
    #if the user has clicked the submit button
    if request.method == "POST":
        form = SignUpForm(request.POST) #this basically takes all that submitted info and put it into a form
        #if the form is valid
        if form.is_valid():
            form.save() #saves the information
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Thanks for creating an account " + username + "\nYou can login below now"))
            return redirect('login')
        #if the form is invalid
        else:
            messages.success(request, ("Error creating account - Please try again"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
    
def update_user(request):
    #if they're logged in, we want to let them be able to update their info
    if request.user.is_authenticated:
        curr_user = User.objects.get(id=request.user.id)    #lookup user in User db model. request.user.id gets a user's id 
        user_form = UpdateUserForm(request.POST or None, instance=curr_user)    #obtain user form

        #if user submits a valid update form
        if user_form.is_valid():
            user_form.save()    #save the user
            login(request, curr_user)   #relog them in (django naunce we have to do when we update a user)
            messages.success(request, ("ChiefUser Has Been Updated"))
            return redirect('home')
        else:   #otherwise we want them to resubmit a valid form
            return render(request, 'update_user.html', {'user_form': user_form})
        
    else:   #if they're not logged in, we want to redirect them to the login page
        messages.success(request, ("Please login to update your account, Chief!"))
        return redirect('home')
    
def update_password(request):
    #check if user is logged in
    if request.user.is_authenticated:
        curr_user = request.user
        #did they fill out form
        if request.method == 'POST':
            form = ChangePasswordForm(curr_user, request.POST)
            #is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, ("Password Updated, Chief! Please log in again"))
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(curr_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, ("Please login to update your password, Chief!"))
        return redirect('home')


    return render(request, 'update_password.html', {})