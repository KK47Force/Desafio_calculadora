from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.views import View
from .forms import CustomUserCreationForm, EmailOrUsernameAuthenticationForm


class CustomLoginView(LoginView):
    template_name = 'tela_login/index.html'
    authentication_form = EmailOrUsernameAuthenticationForm


class Register(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'tela_login/cadastro.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        print('ok')
        messages.success(
            self.request, "Sua conta foi criada com sucesso! Faça login abaixo.")
        return response


def custom_logout_view(request):
    logout(request)
    return redirect('login')  


class SimplePasswordResetView(View):
    def get(self, request):
        return render(request, 'tela_login/password_reset_form.html')

    def post(self, request):
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Por favor, digite um endereço de email.')
            return render(request, 'tela_login/password_reset_form.html')

        try:
            user = User.objects.get(email=email)
            # Armazena o ID do usuário na sessão para usar na próxima etapa
            request.session['reset_user_id'] = user.id
            return redirect('password_reset_confirm_simple')
        except User.DoesNotExist:
            messages.error(
                request, 'Não encontramos uma conta com esse endereço de email.')
            return render(request, 'tela_login/password_reset_form.html')


class SimplePasswordResetConfirmView(View):
    def get(self, request):
        if 'reset_user_id' not in request.session:
            messages.error(request, 'Sessão expirada. Tente novamente.')
            return redirect('password_reset')

        user_id = request.session['reset_user_id']
        try:
            user = User.objects.get(id=user_id)
            form = SetPasswordForm(user)
            return render(request, 'tela_login/password_reset_confirm.html', {'form': form})
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('password_reset')

    def post(self, request):
        if 'reset_user_id' not in request.session:
            messages.error(request, 'Sessão expirada. Tente novamente.')
            return redirect('password_reset')

        user_id = request.session['reset_user_id']
        try:
            user = User.objects.get(id=user_id)
            form = SetPasswordForm(user, request.POST)

            if form.is_valid():
                form.save()
                # Remove o user_id da sessão
                del request.session['reset_user_id']
                messages.success(
                    request, 'Sua senha foi alterada com sucesso!')
                return redirect('password_reset_complete_simple')
            else:
                return render(request, 'tela_login/password_reset_confirm.html', {'form': form})
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('password_reset')


class SimplePasswordResetCompleteView(View):
    def get(self, request):
        return render(request, 'tela_login/password_reset_complete.html')
