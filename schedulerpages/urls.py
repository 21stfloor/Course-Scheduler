from django.urls import path
from .views import register_request, CustomLoginView

urlpatterns = [
    # path('', views.home, name='scheduler-home'),
    path('register/', register_request, name='register'),
    path('login/', CustomLoginView.as_view(), name='login')
]
