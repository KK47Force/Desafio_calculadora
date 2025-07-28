from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(
        url='/accounts/login/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('tela_login.urls')),
    path('calculadora/', include('calculadora.urls')),
]
