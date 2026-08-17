from django.urls import path
from . import views


app_name = "account"
urlpatterns = [
     path('login/', views.UserLogin.as_view(), name='login'),
     path('register/', views.RegisterView.as_view(), name='register'),
     path('verify/', views.VerifyView.as_view(), name='verify'),
     path('logout/', views.user_logout, name='logout'),


]