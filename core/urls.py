from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('tela_login.urls')),
    path('calculadora/', include('calculadora.urls')),
]
