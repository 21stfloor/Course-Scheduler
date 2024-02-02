from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django_tables2 import SingleTableView
from .forms import RegistrationForm
from .models import Course, Departments, Instructor
from .tables import CourseTable

# Create your views here.

def home(request):
    data = Course.objects.all()
    context = {'data': data}
    
    return render(request, 'user/home.html', context)

def course_filter_view(request):
    
    id = request.GET.get('id')
    
    courses = Course.objects.all()
    print(courses)
    if id:
        courses = courses.filter(id=id)
        print(courses)

    departments = Departments.objects.all()
    print(departments)
    
    context = {'courses': courses, 'departments': departments}
    
    #render the django admin override template change_list.html under templates/admin/change_list.html
    
# def instructor_filter_view(request):
#     instructors = Instructor.objects.all()
#     context = {'instructors': instructors}
#     return render(request, 'admin/change_list.html', context)
    
    