from django.shortcuts import render

app_name = 'store'
def home(request):
    return render(request, 'home.html', {})