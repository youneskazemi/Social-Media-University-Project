from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('add_post/', views.AddPost.as_view(), name='add_post'),
    path('delete_post/<post_id>/', views.DeletePost.as_view(), name='delete_post'),
    path('edit_post/<post_id>/', views.EditPost.as_view(), name='edit_post'),
]
