from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add_post/', views.AddPost.as_view(), name='add_post')
]
