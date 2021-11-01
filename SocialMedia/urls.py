from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', include('core.urls', namespace='core')),
    path('oAuth-Google/', include('social_django.urls', namespace='social')),
]


