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
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)
    def get_success_url(self):
        #redirect to user/home.html
        print(self.request.user)
        return reverse('home')
    
def home(request):
    data = Course.objects.all()
    context = {'data': data}
    
    return render(request, 'user/home.html', context)

# class CourseListView(LoginRequiredMixin, SingleTableView):
#     model = Course
#     table_class = CourseTable
#     template_name = 'pages/appointment.html'
#     per_page = 8

#     def post(self, request, *args, **kwargs):
#         pass
#         # pet = Pet.objects.filter(id=request.POST.get('pet')).first()
#         # owner = Customer.objects.filter(email=request.user.email).first()
#         # date = make_aware(datetime.strptime(
#         #             request.POST.get('date'), SCHEDULE_DATEFORMAT), timezone=get_current_timezone())
#         # Course.objects.create(pet=pet, date=date, purpose=request.POST.get('purpose'))
#         # return self.get(request, *args, **kwargs)


#     def get_table_data(self):

#         return Course.objects.all()
    
#     def get_context_data(self, **kwargs):
#         pass
#         # context = super(CourseListView, self).get_context_data(**kwargs)
        
#         # context['form'] = CourseForm(owner=self.request.user)
            
#         # return context
