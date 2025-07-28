from django.urls import path
from tela_login import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('registrar/', views.Register.as_view(), name='signup'),
    path('logout/', views.custom_logout_view, name='logout'),

    # URLs para recuperação de senha 
    path('password_reset/', views.SimplePasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset_confirm/', views.SimplePasswordResetConfirmView.as_view(),
         name='password_reset_confirm_simple'),
    path('password_reset_complete/', views.SimplePasswordResetCompleteView.as_view(),
         name='password_reset_complete_simple'),
]
