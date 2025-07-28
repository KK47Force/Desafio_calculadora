from django.urls import path
from calculadora import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index_calculadora'), # Mapeia a raiz do app 'core'
    path('process_operation/', views.ProcessOperationView.as_view(), name='process_operation'),
]