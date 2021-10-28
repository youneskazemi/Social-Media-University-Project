from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('register/', views.UserRegister.as_view(), name='user_register'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
]
