from django.shortcuts import render

def home(request):
    return render(request, "funk/home.html")