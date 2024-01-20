from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django_tables2 import SingleTableView
from .forms import RegistrationForm
from .models import Course
from .tables import CourseTable

# Create your views here.

def home(request):
    data = Course.objects.all()
    context = {'data': data}
    
    return render(request, 'user/home.html', context)

