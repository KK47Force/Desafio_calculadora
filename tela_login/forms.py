from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model 
from django.contrib.auth import authenticate # Importe authenticate

# Obtém o modelo de usuário atual do Django.
# Isso garante que seu formulário funcione com o User padrão ou um User customizado, se você decidir criar um no futuro.
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    Formulário para criação de usuário personalizado.
    Remove o help_text dos campos padrão e customizados.
    """
    email = forms.EmailField(
        required=True,
        # Remova o help_text daqui
        # help_text='Obrigatório. Digite um endereço de e-mail válido.'
    )

    # Sobrescreve os campos padrão para remover seus help_text
    username = forms.CharField(
        max_length=150,
        # Remova o help_text daqui
        # help_text='Obrigatório. 150 caracteres ou menos. Letras, números e @/.+-/_ apenas.'
    )
    # Importante: password e password2 são instâncias de PasswordInput,
    # eles vêm com help_text por padrão do UserCreationForm.
    # Podemos acessá-los e modificar seus help_text diretamente.
    # Note que UserCreationForm cria password e password2 automaticamente,
    # então você acessa suas propriedades de campo no construtor ou após a inicialização.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o help_text dos campos de senha que são adicionados pela classe pai (UserCreationForm)
        if 'password' in self.fields:
            self.fields['password'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''


    class Meta:
        model = User
        fields = ('username', 'email') # Ajuste aqui se quiser outros campos padrão do User

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este endereço de e-mail já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Tenta autenticar primeiro pelo username
            self.user_cache = authenticate(self.request, username=username, password=password)
            
            if not self.user_cache:
                # Se falhar pelo username, tenta encontrar o usuário pelo email
                try:
                    user = User.objects.get(email=username) # Tenta encontrar pelo email
                except User.DoesNotExist:
                    # Se não encontrar nem pelo username nem pelo email, retorna None
                    pass
                else:
                    # Se encontrar pelo email, tenta autenticar com o username real do usuário
                    self.user_cache = authenticate(self.request, username=user.username, password=password)

            if not self.user_cache:
                # Se a autenticação falhou (usuário/email ou senha incorretos)
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return self.cleaned_data