# myproject/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home2.html')
