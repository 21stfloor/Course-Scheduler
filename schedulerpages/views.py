from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from .forms import RegistrationForm
from .models import Course
# Create your views here.

def register_request(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'user/register.html', {'form':form})

class UserLoginView(LoginView):
    template_name = 'user/login.html'
    
    def get_success_url(self):
        #redirect to user/home.html
        print(self.request.user)
        return reverse('home')
    
def home(request):
    data = Course.objects.all()
    context = {'data': data}
    
    return render(request, 'user/home.html', context)

